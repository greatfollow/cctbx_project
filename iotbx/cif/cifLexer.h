/** \file
 *  This C header file was generated by $ANTLR version 3.2 Sep 23, 2009 12:02:23
 *
 *     -  From the grammar source file : C:\\cctbx_svn\\cctbx_project\\iotbx\\cif\\cif.g
 *     -                            On : 2010-08-25 12:45:36
 *     -                 for the lexer : cifLexerLexer *
 * Editing it, at least manually, is not wise.
 *
 * C language generator and runtime by Jim Idle, jimi|hereisanat|idle|dotgoeshere|ws.
 *
 *
 * The lexer cifLexer has the callable functions (rules) shown below,
 * which will invoke the code for the associated rule in the source grammar
 * assuming that the input stream is pointing to a token/text stream that could begin
 * this rule.
 *
 * For instance if you call the first (topmost) rule in a parser grammar, you will
 * get the results of a full parse, but calling a rule half way through the grammar will
 * allow you to pass part of a full token stream to the parser, such as for syntax checking
 * in editors and so on.
 *
 * The parser entry points are called indirectly (by function pointer to function) via
 * a parser context typedef pcifLexer, which is returned from a call to cifLexerNew().
 *
 * As this is a generated lexer, it is unlikely you will call it 'manually'. However
 * the methods are provided anyway.
 * * The methods in pcifLexer are  as follows:
 *
 *  -  void      pcifLexer->T__31(pcifLexer)
 *  -  void      pcifLexer->T__32(pcifLexer)
 *  -  void      pcifLexer->T__33(pcifLexer)
 *  -  void      pcifLexer->T__34(pcifLexer)
 *  -  void      pcifLexer->T__35(pcifLexer)
 *  -  void      pcifLexer->T__36(pcifLexer)
 *  -  void      pcifLexer->EOL(pcifLexer)
 *  -  void      pcifLexer->DOUBLE_QUOTE(pcifLexer)
 *  -  void      pcifLexer->SINGLE_QUOTE(pcifLexer)
 *  -  void      pcifLexer->ORDINARY_CHAR(pcifLexer)
 *  -  void      pcifLexer->NON_BLANK_CHAR_(pcifLexer)
 *  -  void      pcifLexer->TEXT_LEAD_CHAR(pcifLexer)
 *  -  void      pcifLexer->ANY_PRINT_CHAR(pcifLexer)
 *  -  void      pcifLexer->TAG(pcifLexer)
 *  -  void      pcifLexer->SEMI_COLON_TEXT_FIELD(pcifLexer)
 *  -  void      pcifLexer->DATA_(pcifLexer)
 *  -  void      pcifLexer->SAVE_(pcifLexer)
 *  -  void      pcifLexer->LOOP_(pcifLexer)
 *  -  void      pcifLexer->GLOBAL_(pcifLexer)
 *  -  void      pcifLexer->STOP_(pcifLexer)
 *  -  void      pcifLexer->VERSION(pcifLexer)
 *  -  void      pcifLexer->DATA_BLOCK_HEADING(pcifLexer)
 *  -  void      pcifLexer->SAVE_FRAME_HEADING(pcifLexer)
 *  -  void      pcifLexer->SAVE(pcifLexer)
 *  -  void      pcifLexer->SINGLE_QUOTED_STRING(pcifLexer)
 *  -  void      pcifLexer->DOUBLE_QUOTED_STRING(pcifLexer)
 *  -  void      pcifLexer->DIGIT(pcifLexer)
 *  -  void      pcifLexer->EXPONENT(pcifLexer)
 *  -  void      pcifLexer->UNQUOTED_STRING(pcifLexer)
 *  -  void      pcifLexer->CHAR_STRING(pcifLexer)
 *  -  void      pcifLexer->COMMENTS(pcifLexer)
 *  -  void      pcifLexer->NON_BLANK_CHAR(pcifLexer)
 *  -  void      pcifLexer->WHITESPACE(pcifLexer)
 *  -  void      pcifLexer->Tokens(pcifLexer)
 *
 * The return type for any particular rule is of course determined by the source
 * grammar file.
 */
// [The "BSD licence"]
// Copyright (c) 2005-2009 Jim Idle, Temporal Wave LLC
// http://www.temporal-wave.com
// http://www.linkedin.com/in/jimidle
//
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions
// are met:
// 1. Redistributions of source code must retain the above copyright
//    notice, this list of conditions and the following disclaimer.
// 2. Redistributions in binary form must reproduce the above copyright
//    notice, this list of conditions and the following disclaimer in the
//    documentation and/or other materials provided with the distribution.
// 3. The name of the author may not be used to endorse or promote products
//    derived from this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
// IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
// OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
// IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
// INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
// NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
// THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

#ifndef _cifLexer_H
#define _cifLexer_H
/* =============================================================================
 * Standard antlr3 C runtime definitions
 */
#include    <antlr3.h>

/* End of standard antlr 3 runtime definitions
 * =============================================================================
 */

#if defined(min) && defined(max)
  #define min_redefined min
  #define max_redefined max
  #undef min
  #undef max
#endif
#include <scitbx/array_family/shared.h>
#ifdef min_redefined
  #define max max_redefined
  #define min min_redefined
#endif



#ifdef __cplusplus
extern "C" {
#endif

// Forward declare the context typedef so that we can use it before it is
// properly defined. Delegators and delegates (from import statements) are
// interdependent and their context structures contain pointers to each other
// C only allows such things to be declared if you pre-declare the typedef.
//
typedef struct cifLexer_Ctx_struct cifLexer, * pcifLexer;



#ifdef  ANTLR3_WINDOWS
// Disable: Unreferenced parameter,                                                     - Rules with parameters that are not used
//          constant conditional,                                                       - ANTLR realizes that a prediction is always true (synpred usually)
//          initialized but unused variable                                     - tree rewrite variables declared but not needed
//          Unreferenced local variable                                         - lexer rule declares but does not always use _type
//          potentially unitialized variable used                       - retval always returned from a rule
//                      unreferenced local function has been removed    - susually getTokenNames or freeScope, they can go without warnigns
//
// These are only really displayed at warning level /W4 but that is the code ideal I am aiming at
// and the codegen must generate some of these warnings by necessity, apart from 4100, which is
// usually generated when a parser rule is given a parameter that it does not use. Mostly though
// this is a matter of orthogonality hence I disable that one.
//
#pragma warning( disable : 4100 )
#pragma warning( disable : 4101 )
#pragma warning( disable : 4127 )
#pragma warning( disable : 4189 )
#pragma warning( disable : 4505 )
#pragma warning( disable : 4701 )
#endif

/* ========================
 * BACKTRACKING IS ENABLED
 * ========================
 */

/** Context tracking structure for cifLexer
 */
struct cifLexer_Ctx_struct
{
    /** Built in ANTLR3 context tracker contains all the generic elements
     *  required for context tracking.
     */
    pANTLR3_LEXER    pLexer;


     void (*mT__31)     (struct cifLexer_Ctx_struct * ctx);
     void (*mT__32)     (struct cifLexer_Ctx_struct * ctx);
     void (*mT__33)     (struct cifLexer_Ctx_struct * ctx);
     void (*mT__34)     (struct cifLexer_Ctx_struct * ctx);
     void (*mT__35)     (struct cifLexer_Ctx_struct * ctx);
     void (*mT__36)     (struct cifLexer_Ctx_struct * ctx);
     void (*mEOL)       (struct cifLexer_Ctx_struct * ctx);
     void (*mDOUBLE_QUOTE)      (struct cifLexer_Ctx_struct * ctx);
     void (*mSINGLE_QUOTE)      (struct cifLexer_Ctx_struct * ctx);
     void (*mORDINARY_CHAR)     (struct cifLexer_Ctx_struct * ctx);
     void (*mNON_BLANK_CHAR_)   (struct cifLexer_Ctx_struct * ctx);
     void (*mTEXT_LEAD_CHAR)    (struct cifLexer_Ctx_struct * ctx);
     void (*mANY_PRINT_CHAR)    (struct cifLexer_Ctx_struct * ctx);
     void (*mTAG)       (struct cifLexer_Ctx_struct * ctx);
     void (*mSEMI_COLON_TEXT_FIELD)     (struct cifLexer_Ctx_struct * ctx);
     void (*mDATA_)     (struct cifLexer_Ctx_struct * ctx);
     void (*mSAVE_)     (struct cifLexer_Ctx_struct * ctx);
     void (*mLOOP_)     (struct cifLexer_Ctx_struct * ctx);
     void (*mGLOBAL_)   (struct cifLexer_Ctx_struct * ctx);
     void (*mSTOP_)     (struct cifLexer_Ctx_struct * ctx);
     void (*mVERSION)   (struct cifLexer_Ctx_struct * ctx);
     void (*mDATA_BLOCK_HEADING)        (struct cifLexer_Ctx_struct * ctx);
     void (*mSAVE_FRAME_HEADING)        (struct cifLexer_Ctx_struct * ctx);
     void (*mSAVE)      (struct cifLexer_Ctx_struct * ctx);
     void (*mSINGLE_QUOTED_STRING)      (struct cifLexer_Ctx_struct * ctx);
     void (*mDOUBLE_QUOTED_STRING)      (struct cifLexer_Ctx_struct * ctx);
     void (*mDIGIT)     (struct cifLexer_Ctx_struct * ctx);
     void (*mEXPONENT)  (struct cifLexer_Ctx_struct * ctx);
     void (*mUNQUOTED_STRING)   (struct cifLexer_Ctx_struct * ctx);
     void (*mCHAR_STRING)       (struct cifLexer_Ctx_struct * ctx);
     void (*mCOMMENTS)  (struct cifLexer_Ctx_struct * ctx);
     void (*mNON_BLANK_CHAR)    (struct cifLexer_Ctx_struct * ctx);
     void (*mWHITESPACE)        (struct cifLexer_Ctx_struct * ctx);
     void (*mTokens)    (struct cifLexer_Ctx_struct * ctx);    const char * (*getGrammarFileName)();
    void            (*free)   (struct cifLexer_Ctx_struct * ctx);


        scitbx::af::shared<std::string> *errors;

};

// Function protoypes for the constructor functions that external translation units
// such as delegators and delegates may wish to call.
//
ANTLR3_API pcifLexer cifLexerNew         (pANTLR3_INPUT_STREAM instream);
ANTLR3_API pcifLexer cifLexerNewSSD      (pANTLR3_INPUT_STREAM instream, pANTLR3_RECOGNIZER_SHARED_STATE state);

/** Symbolic definitions of all the tokens that the lexer will work with.
 * \{
 *
 * Antlr will define EOF, but we can't use that as it it is too common in
 * in C header files and that would be confusing. There is no way to filter this out at the moment
 * so we just undef it here for now. That isn't the value we get back from C recognizers
 * anyway. We are looking for ANTLR3_TOKEN_EOF.
 */
#ifdef  EOF
#undef  EOF
#endif
#ifdef  Tokens
#undef  Tokens
#endif
#define DOUBLE_QUOTED_STRING      29
#define CHAR_STRING      13
#define EXPONENT      12
#define NON_BLANK_CHAR      27
#define SEMI_COLON_TEXT_FIELD      14
#define SINGLE_QUOTED_STRING      28
#define DOUBLE_QUOTE      16
#define GLOBAL_      24
#define ORDINARY_CHAR      18
#define WHITESPACE      5
#define SAVE      7
#define VERSION      26
#define EOF      -1
#define TAG      8
#define SINGLE_QUOTE      17
#define T__31      31
#define T__32      32
#define T__33      33
#define EOL      15
#define STOP_      25
#define T__34      34
#define NON_BLANK_CHAR_      19
#define COMMENTS      4
#define T__35      35
#define SAVE_FRAME_HEADING      6
#define T__36      36
#define TEXT_LEAD_CHAR      20
#define ANY_PRINT_CHAR      21
#define SAVE_      23
#define LOOP_      10
#define DIGIT      11
#define UNQUOTED_STRING      30
#define DATA_      22
#define DATA_BLOCK_HEADING      9
#ifdef  EOF
#undef  EOF
#define EOF     ANTLR3_TOKEN_EOF
#endif

#ifndef TOKENSOURCE
#define TOKENSOURCE(lxr) lxr->pLexer->rec->state->tokSource
#endif

/* End of token definitions for cifLexer
 * =============================================================================
 */
/** \} */

#ifdef __cplusplus
}
#endif

#endif

/* END - Note:Keep extra line feed to satisfy UNIX systems */
