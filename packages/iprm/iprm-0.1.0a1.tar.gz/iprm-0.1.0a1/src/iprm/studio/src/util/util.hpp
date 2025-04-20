/*
 * Copyright (c) 2025 ayeteadoe <ayeteadoe@gmail.com>
 *
 * SPDX-License-Identifier: MIT
 */
#pragma once

template <class... Ts>
struct overloaded : Ts... {
  using Ts::operator()...;
};
