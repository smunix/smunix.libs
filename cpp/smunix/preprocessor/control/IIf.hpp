/*
 * Copyright (C) 2011 Providence M. Salumu
 *
 * Permission to use, copy, modify, and/or distribute this software for any
 * purpose with or without fee is hereby granted, provided that the above
 * copyright notice and this permission notice appear in all copies.
 *
 * THE SOFTWARE IS PROVIDED AS IS AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 * WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 * MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 * ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 * WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 * ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 * OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
 * 
 *  /smunix.cpp/preprocessor/control/IIf.hpp
 *  Created on: Mar 26, 2011, 11:09:10 AM
 */


#ifndef IIF_HPP_
#define IIF_HPP_

#  define SMUNIX_PP_IIF(b, t, f) SMUNIX_PP_IIF_I (b, t, f)
#  define SMUNIX_PP_IIF_I(b, t, f) SMUNIX_PP_IIF_ ## b (t, f)

#  define SMUNIX_PP_IIF_1(t, f) t
#  define SMUNIX_PP_IIF_0(t, f) f

#endif /* IIF_HPP_ */
