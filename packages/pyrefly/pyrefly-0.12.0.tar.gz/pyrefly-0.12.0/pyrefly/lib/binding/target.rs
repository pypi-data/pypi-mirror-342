/*
 * Copyright (c) Meta Platforms, Inc. and affiliates.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */

use ruff_python_ast::Expr;
use ruff_text_size::Ranged;
use ruff_text_size::TextRange;

use crate::binding::binding::Binding;
use crate::binding::binding::BindingExpect;
use crate::binding::binding::ExprOrBinding;
use crate::binding::binding::Key;
use crate::binding::binding::KeyAnnotation;
use crate::binding::binding::KeyExpect;
use crate::binding::binding::SizeExpectation;
use crate::binding::binding::UnpackedPosition;
use crate::binding::bindings::BindingsBuilder;
use crate::binding::scope::FlowStyle;
use crate::error::kind::ErrorKind;
use crate::graph::index::Idx;

impl<'a> BindingsBuilder<'a> {
    fn bind_unpacking(
        &mut self,
        elts: &[Expr],
        make_binding: &dyn Fn(Option<Idx<KeyAnnotation>>) -> Binding,
        range: TextRange,
    ) {
        // We are going to use this binding many times, so compute it once.
        let key = self.table.insert(Key::Unpack(range), make_binding(None));

        // An unpacking has zero or one splats (starred expressions).
        let mut splat = false;
        for (i, e) in elts.iter().enumerate() {
            match e {
                Expr::Starred(e) => {
                    splat = true;
                    // Counts how many elements are after the splat.
                    let j = elts.len() - i - 1;
                    let make_nested_binding = |_: Option<Idx<KeyAnnotation>>| {
                        Binding::UnpackedValue(key, range, UnpackedPosition::Slice(i, j))
                    };
                    self.bind_target(&e.value, &make_nested_binding, None);
                }
                _ => {
                    let idx = if splat {
                        // If we've encountered a splat, we no longer know how many values have been consumed
                        // from the front, but we know how many are left at the back.
                        UnpackedPosition::ReverseIndex(elts.len() - i)
                    } else {
                        UnpackedPosition::Index(i)
                    };
                    let make_nested_binding =
                        |_: Option<Idx<KeyAnnotation>>| Binding::UnpackedValue(key, range, idx);
                    self.bind_target(e, &make_nested_binding, None);
                }
            }
        }
        let expect = if splat {
            SizeExpectation::Ge(elts.len() - 1)
        } else {
            SizeExpectation::Eq(elts.len())
        };
        self.table.insert(
            KeyExpect(range),
            BindingExpect::UnpackedLength(key, range, expect),
        );
    }

    /// Bind the LHS of a target in a syntactic form (e.g. assignments, variables
    /// bound in a `for`` loop header, variables defined by a `with` statement header).
    ///
    /// The `target` is the LHS. It is an `Expr`, but in fact only a handful of forms
    /// are legal because targets can only be names, attributes, subscripts, or unpackings. An
    /// example target illustrating all of the cases is `(x.y, d["k"], [z, *w, q])`
    ///
    /// The `make_binding` function is a callback to the caller, who is responsible for constructing
    /// a binding that provides the value of the RHS. To handle cases where the type of the LHS
    /// is restricted, it takes an optional `KeyAnnotation` which should be the annotation for the
    /// target when one is available.
    ///
    /// The `value` argument is only provided when handling top-level assignment targets;
    /// it enables contextual typing. At the moment it is only used in the attribute case (because
    /// the other cases instead rely on `make_binding` to handle contextual typing, which works
    /// when the form is not an unpacking but results in false negatives when it is).
    ///
    /// TODO(stroxler): The way this is wired up does not work well in
    /// the general case of an unpacking. The attempt to pass around a `make_binding`
    /// callable for both inference and checking does not compose properly with `bind_unpacking`,
    /// because for an unpack target there is no annotation for the entire RHS.
    /// As a result, for all cases except attributes we wind up ignoring type errors
    /// when the target is an unpacking pattern.
    pub fn bind_target_controlling_errors(
        &mut self,
        target: &Expr,
        make_binding: &dyn Fn(Option<Idx<KeyAnnotation>>) -> Binding,
        value: Option<&Expr>,
        add_error: bool,
    ) {
        match target {
            Expr::Name(name) => self.bind_assign(name, make_binding, FlowStyle::None),
            Expr::Attribute(x) => {
                // `make_binding` will give us a binding for inferring the value type, which we
                // *might* use to compute the attribute type if there are no explicit annotations.
                let attr_value = if let Some(value) = value {
                    ExprOrBinding::Expr(value.clone())
                } else {
                    ExprOrBinding::Binding(make_binding(None))
                };
                // Create a check binding to verify that the assignment is valid.
                self.table.insert(
                    KeyExpect(x.range),
                    BindingExpect::CheckAssignToAttribute(Box::new((
                        x.clone(),
                        attr_value.clone(),
                    ))),
                );
                // If this is a self-assignment, record it because we may use it to infer
                // the existence of an instance-only attribute.
                self.record_self_attr_assign(x, attr_value, None);
            }
            Expr::Subscript(x) => {
                let binding = make_binding(None);
                self.table.insert(
                    Key::Anon(x.range),
                    Binding::SubscriptValue(Box::new(binding), x.clone()),
                );
            }
            Expr::Tuple(tup) => {
                self.bind_unpacking(&tup.elts, make_binding, tup.range);
            }
            Expr::List(lst) => {
                self.bind_unpacking(&lst.elts, make_binding, lst.range);
            }
            Expr::Starred(x) => {
                if add_error {
                    self.error(
                        x.range,
                        "Starred assignment target must be in a list or tuple".to_owned(),
                        ErrorKind::InvalidSyntax,
                    )
                };
                self.bind_target_controlling_errors(&x.value, make_binding, value, add_error);
            }
            _ => {
                if add_error {
                    self.error(
                        target.range(),
                        "Invalid assignment target".to_owned(),
                        ErrorKind::InvalidSyntax,
                    )
                }
            }
        }
    }

    pub fn bind_target(
        &mut self,
        target: &Expr,
        make_binding: &dyn Fn(Option<Idx<KeyAnnotation>>) -> Binding,
        value: Option<&Expr>,
    ) {
        self.bind_target_controlling_errors(target, make_binding, value, true)
    }
}
