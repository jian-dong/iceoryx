// Copyright (c) 2022 by Apex.AI Inc. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// SPDX-License-Identifier: Apache-2.0
#ifndef IOX_DUST_STRING_CONVERSION_INL
#define IOX_DUST_STRING_CONVERSION_INL

#include "iceoryx_dust/cxx/string_conversion.hpp"

namespace iox
{
namespace cxx
{
template <typename F, typename T>
inline constexpr T convert(const F value)
{
    return From<F, T>::convertInternal(value);
}

template <uint64_t N>
inline std::string From<string<N>, std::string>::convertInternal(const string<N>& value)
{
    return std::string(value.c_str(), value.size());
}

template <uint64_t N>
inline string<N> From<std::string, string<N>>::convertInternal(const std::string& value) noexcept
{
    return string<N>(TruncateToCapacity, value.c_str(), value.size());
}
} // namespace cxx
} // namespace iox

#endif // IOX_DUST_STRING_CONVERSION_INL
