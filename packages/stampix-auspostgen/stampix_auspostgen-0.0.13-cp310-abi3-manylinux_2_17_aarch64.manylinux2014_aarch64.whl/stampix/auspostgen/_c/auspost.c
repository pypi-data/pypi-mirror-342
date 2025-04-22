/*---------------------------------------------------------------------------
 * Title    : Australia Post Barcode Demonstration.
 * Version  : r2
 * Date     : 5th March 1999.
 * Language : C (ANSI)
 *
 * Description
 * -----------
 * This software module generates 4-states barcode digits with Reed-Solomon
 * error detection and correction algorithm.
 *
 * It includes a main program for demonstrating barcode generation.
 * The program prompts the user for the Format Control Code, the sorting
 * code and optionally, a User Information String.  It then invokes
 * the routine BuildBarcode to generate the barcode string.
 *
 * Disclaimer
 * ----------
 * Whilst Australia Post provides this program in good faith, no
 * responsibility is taken as to its accuracy. The program is
 * provided for guidance only. Australia Post shall not be liable
 * for any loss or damage arising from the use of, or reliance placed
 * on, any information provided by it.
 *
 * History    By            Ref    Description
 * --------   ----------    ---    ------------------------------------------
 * 22/10/97   S Seniors     R0     Original version.
 * 18/02/98   H Nguyen      R1     Revision 1 based on 11/97 issue of Spec 203
 *                                 Remove input params LodgementNo, ProductType,
 *                                 CustInfoBars and FCC 33 & 70.
 * 02/03/99   D Warring     R2     Revision 2 based on feedback and testing
 *                                 - Corrections to character conversions.
 *                                 - Added barcode calculator main program.
---------------------------------------------------------------------------*/
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define true 1
#define false 0

/*
 * Set BC_DEMO to 0, to exclude the main program barcode calculater
 * You may wish to do this if you want to build this as an object library
 */

#define BC_DEMO 1

/*
 * FCC_nn_type:
 * Decimal representation of the format control field for barcode types,
 * as defined in Australia Post Specification 203
 */
#define FCC_37_CUST           "11"
#define FCC_37_ROUT           "87"
#define FCC_37_REPL           "45"
#define FCC_37_REDI           "92"
#define FCC_52_FF_MET         "59"
#define FCC_67_FF_MET         "62"
#define FCC_67_FF_MAN         "44"

/*
 * Barcode stop and start symbols - always constant.
 */
#define BC_START_SYM          "13"
#define BC_STOP_SYM           "13"

/*
 * Return status codes for barcode routines. See bcmsg below for the
 * corresponding messages.
 */
#define BC_OK                 0
#define BC_INV_FCC            1
#define BC_INV_SORT_CODE      2
#define BC_INV_CUST_INFO      3
#define BC_INV_ENCODE_STR     4
#define BC_INV_RANGE          5

char *bcmsg[] = {
        "Barcode successfully encoded",
        "Invalid Format Control field",
        "Invalid Sorting Code field",
        "Invalid customer information field",
        "Unable to encode data",
        "Invalid barcode range",
        };

/*
 * Structure for the 4 parity symbols of the Reed-Solomon error
 * correction block.
 */
typedef struct paritystring{
        unsigned int in[4];
} paritystring;

/* Global variables: The multiplication table for Galois field
 * arithmetic and the generator polynomial, g(x)
 */

static int mult[64][64];
static int gen[5] = {0,0,0,0,0};

#define BSET "0123"

/*
 * Character set and barcode symbol tables for N and C encoding of digits
 */
#define NSET "01234567890"
static char *NTable[10] = {"00", "01", "02", "10", "11", "12", "20", "21", "22", "30"};
/*
 * CN-table for encoding numerics using the C-table
 */
static char *CNTable[10] = {"222", "300", "301", "302", "310", "311", "312", "320",
                     "321", "322"};

/*
 * Character set and barcode symbol tables for Z and C encoding of
 * uppercase alphabetic characters.
 */
#define ZSET "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
static char *ZTable[26] = {       /* Z-Table for encoding uppercase alphas */
  "000", "001", "002", "010", "011", "012", "020", "021", "022", "100", "101"
, "102", "110", "111", "112", "120", "121", "122", "200", "201", "202", "210"
, "211", "212", "220", "221"};

/*
 * Character set and barcode symbol table for C encoding of
 * lowercase alphabetic characters.
 */
#define CSET "abcdefghijklmnopqrstuvwxyz #"
static char *CTable[28] = {     /* C-table for encoding lowercase alphas */
 "023", "030", "031", "032", "033", "103", "113", "123", "130", "131", "132"
,"133", "203", "213", "223", "230", "231", "232", "233", "303", "313", "323"
, "330", "331", "332", "333", "003", "013"};

/*
 * Encoding table for G3 Decimal conversion of barcode symbols. This is used
 * for Reed-Solomon error correction calculations.
 */
static char *BarTable[64] = {
  "000", "001", "002", "003", "010", "011", "012", "013", "020", "021", "022"
, "023", "030", "031", "032", "033", "100", "101", "102", "103", "110", "111"
, "112", "113", "120", "121", "122", "123", "130", "131", "132", "133", "200"
, "201", "202", "203", "210", "211", "212", "213", "220", "221", "222", "223"
, "230", "231", "232", "233", "300", "301", "302", "303", "310", "311", "312"
, "313", "320", "321", "322", "323", "330", "331", "332", "333"};

/*---------------------------------------------------------------------------
 * RSInitialise:
 * Initialises the Reed-Solomon Parity generator.  The code in this function
 * has been supplied by Australia Post Operations Engineering.
 *---------------------------------------------------------------------------*/

void RSInitialise () {
    unsigned int primpoly, test, prev, next;
        int     i, j;

               /* Set up the constants required.  primpoly is the binary
                * representation of the primitive polynomial used to construct
                * the Galois field GF(64). Test is used to check when an
                * element must be reduced modulo primpoly.
                */

        primpoly = 67;
        test = 64;

               /* The mult[][] array provides lookup table multiplication in
                * GF(64). The two array indices are the elements to be
                * multiplied, and the corresponding value is the product.
                * Mult a field element by 0 is 0 and mult by 1 is itself
                */

        for (i = 0; i < 64; i++) {
                mult[0][i] = 0;
                mult[1][i] = i;
        }

               /* Multiplication by elements other than 0 or 1 requires the
                * corresponding powers of alpha which is a root of primpoly.
                *
                * Beginning with the zero power of alpha, which is 1,
                * successive powers of alpha are obtained by shifting to the
                * left. If the result exceeds 6 bits, then it is reduced modulo
                * primpoly.  The rows of mult[][] are filled iteratively
                * according to these powers.  Note that the `powers of alpha'
                * representation is logarithmic, so that multiplication
                * requires just an addition.  prev is the previous power of
                * alpha, and next is the next power.  Because of the above
                * mentioned property of logarithms, the next row is just the
                * prev row shifted to the left.
                */

        prev = 1;
        for (i = 1; i < 64; i++) {
                next = prev << 1;
                if (next & test)
                        next ^= primpoly;
                for (j = 0; j < 64; j++) {
                        mult[next][j] = mult[prev][j]<<1;
                        if (mult[next][j] & test)
                                mult[next][j] ^= primpoly;
                }
                prev = next;
        }

        gen[0] = 48;   /* Initialise the generator polynomial */
        gen[1] = 17;
        gen[2] = 29;
        gen[3] = 30;
        gen[4] = 1;

        return;
 }

/*---------------------------------------------------------------------------
 * RSEncode:
 * Generates the Reed-Solomon Parity Symbols.
 * NOTE: This code in this function has been supplied by Australia Post
 * Operations Engineering.
 *---------------------------------------------------------------------------*/

paritystring RSEncode (int Num_infosym, unsigned int infosymbols[])
{
        int     n, k, i, j;
        unsigned int temp[31];
        paritystring parity4;

	if (gen[0] == 0) {
		RSInitialise();
	}

        k = Num_infosym;       /* Calc the code params n & k from Num_infosym */
        n = k+4;

               /* The temp array is initialised with x^(n-k) m(x).  After
                * division by g(x), temp will contain the parity symbols,
                * p(x), in locations 0 to 4. Note that p(x) is the remainder
                * after the division operation.
                */

    for (i = 0; i < 4; i++)
        temp[i] = 0;
        for (i = 4; i < n; i++)
                temp[i] = infosymbols[i - 4];

               /* Perform the division by the generator polynomial g(x).
                * This is accomplished using k iterations of long division,
                * where g(x) times the most significant symbol in the
                * dividend are subtracted.
                */

        for (i = k-1; i >= 0; i--) {
                for (j = 0; j <= 4; j++) {
                        temp[i + j] = temp[i + j] ^ (mult[gen[j]][temp[4 + i]]);
                }
        }

        for (i = 0; i < 4; i++)    /* Place the parity symbols in the array */
                parity4.in[i] = temp[i];

        return(parity4);
}


/*---------------------------------------------------------------------------
 * AppendRSParity:
 *
 * This function is used to calculate and append RS Parity Symbols to a
 * barcode string.  It should be called all data has been encoded, to
 * append the parity symbols for the Reed-Solomon error correction block.
 *
 * It acheives this by:
 * -- converting each group of 3 bars into their decimal equivalents.
 * -- calling the RSEncode function to generate the 4 parity symbols.
 * -- converting the parity symbols to their group of 3 bars equivalent
 * -- appending the parity bars to the end of the original barcode.
 *
 * NOTE:
 * (1)    This function ignores the first two characters. It is assumed
 *        that they are start symbols.
 * (2)    It is also assumed that the last 14 characters are reserved for
 *        the parity symbols and the stop bits.
 * (3)    The RSEncode function follows the AP Spec 203 notation, where the
 *        codeword symbols are indexed, left to right, as Cn-1 .. C0.  The
 *        four parity symbols are thus C3 .. C0. This is reversed on input
 *        and output to RSEncode to the conventional left to right array
 *	  array representation of a string as bc[0] .. bc[n-1].
 *---------------------------------------------------------------------------*/
int AppendRSParity(
         char *sBarcode,        /* Input/output barcode */
         int iBarLength)        /* Target barcode length, including space
                                 * for parity, start and stop symbols */
{
        int iSymbols;
        int iNumInfoSymbols;
        int i, j;
        int bcstat = BC_OK;
        int bcfound;
        char sBarGroup[4] = "";
        unsigned int iCodeWord[31];
        unsigned int iTempCodeWord[31];
        paritystring paritysymbols;

        /* Calc the number of symbols & info symbols for the barcode */
        iSymbols = (iBarLength - 4) / 3;
        iNumInfoSymbols = iSymbols - 4;

        /* For the purposes of RS Parity generation the barcode string
         * consists of a number of 3 bar information symbols. Each
         * group of 3 bars must be converted to it's decimal equivalent.
         * This is performed by:
         * -- setting sBarGroup to the 3 bars
         * -- comparing elements of sBarGroup to BarTable toe find a match
         * -- iCodeWord[i] is then set to the match position in BarTable
         */

        for (i=0; i<iNumInfoSymbols; i++)
        {
                strncpy(sBarGroup, sBarcode + 2 + (i*3), 3);
                sBarGroup[3] = 0;
                bcfound = false;


                for (j=0; j<64; j++)
                {
                        if (strncmp(BarTable[j], sBarGroup, 3) == 0)
                        {
                                iCodeWord[i] = j;
                                bcfound = true;
                                break;
                        }
                }
                if (bcfound != true) {
                        iCodeWord[i] = 0;
                        bcstat = BC_INV_ENCODE_STR;
                }
        }

        /* Set the parity check symbols to zero in the code word */
        for (i=iNumInfoSymbols; i<iSymbols; i++)
                iCodeWord[i] = 0;

        /* Now we must convert the symbol order from 1,2,3.. to ..3,2,1 */
        j = iNumInfoSymbols - 1;
        for (i=0; i<iNumInfoSymbols; i++)
                iTempCodeWord[i] = iCodeWord[j--];

        /* Call RSEncode to get the parity symbols */
        paritysymbols = RSEncode(iNumInfoSymbols, iTempCodeWord);

        /* Add the RS Parity Symbols to the end of the code word */
        /* Convert the symbol order from 1,2,3.. to ..3,2,1 */

        for (i=0; i<4; i++)  {
                iCodeWord[i+iNumInfoSymbols] = paritysymbols.in[3-i];
        }

        /* Now we need to grab the 4 parity symbols returned
        & append them to our bar code string */
        for (i=iNumInfoSymbols; i<iSymbols; i++)

                strncpy (sBarcode + 2 + (i*3), BarTable[iCodeWord[i]], 3);

        return bcstat;
}

/*---------------------------------------------------------------------------
 * Lookup:
 * Return a character ordinance number
 *---------------------------------------------------------------------------*/
static int lookup(char *set, char ch, int *idx) {
	char *pos;
	pos = strchr (set, ch);
	if (pos != NULL) {
		*idx = pos - set;
		return true;
	}
	else {
		return false;
	}
}
/*---------------------------------------------------------------------------
 * ConvertFill:
 * Insert barcode fill characters into the given range, '333..'.
 *---------------------------------------------------------------------------*/
int ConvertFill (
        char *sBarcoded,         /* Returned barcode. */
        int istart, int iend)    /* Range to write in barcode (offset from 1) */
{
        int ipos;

        if (istart <= 0 || istart > iend) {
		return BC_INV_RANGE;
        }

        for (ipos = istart - 1; ipos < iend;) {
                sBarcoded[ipos++] = '3';
        }
        return BC_OK;
}

/*---------------------------------------------------------------------------
 * ConvertB:
 * Straight insertion of pre-converted barcode symbols.
 * -- Consumes (istart - iend + 1) input characters.
 *---------------------------------------------------------------------------*/
int ConvertB (
        char *sBarcoded,         /* Returned barcode. */
        int istart, int iend,    /* Range to write in barcode (offset from 1) */
        char *InString)
{
        int i;
        int ipos;
        int bcstat = BC_OK;

        if (istart <= 0 || istart > iend) {
		return BC_INV_RANGE;
        }

        for (i = 0,ipos = istart - 1; (ipos+1) <= iend; i++) {
                if (InString[i] == '\0') {
                        /* End of string. Fill remainder of barcode string */
                        break;
                }
                else if (strchr(BSET, InString[i])) {
                        sBarcoded[ipos++] = InString[i];
                }
                else
                {
                        sBarcoded[ipos++] = ' ';
                        bcstat = BC_INV_ENCODE_STR;
                }
        }

        if (ipos < iend) {
                ConvertFill(sBarcoded, ipos+1, iend);
        }
        return bcstat;
}

/*---------------------------------------------------------------------------
 * ConvertN:
 * Converts the number of characters specified in iNumChars using N-Table.
 * -- Consumes (istart - iend + 1) * 2 input characters.
 ---------------------------------------------------------------------------*/
int ConvertN (
        char *sBarcoded,         /* Returned barcode. */
        int istart, int iend,    /* Range to write in barcode (offset from 1) */
        char *InString)          /* Input number string: Character set [0-9] */
{
        int i, j;
        int ipos;
        char *barval;
        int bcstat = BC_OK;
	int iCellSize = 2;
	int idx;

        if (istart <= 0 || istart > iend) {
		return BC_INV_RANGE;
        }

        for (i=0,ipos = istart-1; (ipos+iCellSize) <= iend; i++)
        {
                if (lookup(NSET, InString[i], &idx))
                {
                        barval = NTable[idx];
                }
                else {
                        barval = "  ";
                        bcstat = BC_INV_ENCODE_STR;
                }

		for (j = 0; j < iCellSize; j++) {
			sBarcoded[ipos++] = barval[j];
		}
        }

	if (ipos != iend) {
		bcstat = BC_INV_RANGE;
	}

        return bcstat;
}

/*---------------------------------------------------------------------------
 * ConvertZ:
 * Convert characters to bar values using the Z-Table.
 * -- Consumes up to (istart - iend + 1) * 3 input characters.
 * -- The input string can be terminated by a null character. The resulting
 *    barcode string will then be padded with '3' characters.
 *---------------------------------------------------------------------------*/
int ConvertZ (
        char *sBarcoded,         /* Returned barcode string. */
        int istart, int iend,    /* Range to write in barcode (offset from 1) */
        char *InString)          /* Input string. Characters [A-Z] */
{
        int i, j;
        char *barval;
        int ipos;
        int bcstat = BC_OK;
	int iCellSize = 3;
	int idx;

        if (istart <= 0 || istart > iend) {
		return BC_INV_RANGE;
        }

        for (i=0,ipos=istart-1; (ipos+iCellSize) <= iend; i++)
        {
                if (InString[i] == '\0') {
                        /* End of string. Fill remainder of barcode string */
                        break;
                }
                else if (lookup(ZSET, InString[i], &idx))
                {
                        barval = ZTable[idx];
                }
                else {
                        barval = "   ";
                        bcstat = BC_INV_ENCODE_STR;
                }

		for (j = 0; j < iCellSize; j++) {
			sBarcoded[ipos++] = barval[j];
		}
        }

        if (ipos < iend) {
                ConvertFill(sBarcoded, ipos+1, iend);
        }
        return bcstat;
}


/*---------------------------------------------------------------------------
 * ConvertC:
 * Convert characters to bar values using the C-Table
 * -- Consumes up to (istart - iend + 1) * 3 input characters.
 * -- The input string can be terminated by a null character. The resulting
 *    barcode string will then be padded with '3' characters.
 *---------------------------------------------------------------------------*/
int ConvertC (
        char *sBarcoded,     /* Returned barcode. */
        int istart, int iend,/* Range to write in barcode (offset from 1) */
        char *InString)      /* Input number string: Characters [a-zA-Z0-9 #] */
{
        int i, j;
        int ipos;
        char c;
        char *barval;
        int bcstat = BC_OK;
	int iCellSize = 3;
	int idx;

        if (istart <= 0 || istart > iend) {
		return BC_INV_RANGE;
        }

        for (i=0, ipos=istart-1; (ipos+iCellSize) <= iend; i++) {

                c = InString[i];

                if (c == '\0') {
                        /* End of string. Fill remainder of barcode string */
                        break;
                }
                else if (isupper(c) &&  lookup(ZSET, InString[i], &idx))
                {
			/* Uppercase */
                        barval = ZTable[idx];
                }
                else if (isdigit(c) && lookup(NSET, InString[i], &idx))
                {
			/* Digits */
                        barval = CNTable[idx];
                }
                else if (lookup(CSET, InString[i], &idx))
                {
			/* Lowercase & miscellaneous characters */
                        barval = CTable[idx];
                }
                else
                {
                        barval = "   ";
                        bcstat = BC_INV_ENCODE_STR;
                }

		for (j = 0; j < iCellSize; j++) {
			sBarcoded[ipos++] = barval[j];
		}
        }

        if (ipos < iend) {
                ConvertFill(sBarcoded, ipos+1, iend);
        }
        return bcstat;
}

/*---------------------------------------------------------------------------
 * BuildBarcode37:
 * Build a length 37 barcode from an FCC and a sorting code
 *---------------------------------------------------------------------------*/
int BuildBarcode37(
    char *sBarcode,		/* Output barcode buffer, length >= 38 chars */
    char *sFCC,                 /* Input FCC, 2 decimal digits */
    char *sSortingCode)         /* Input Sorting code, 8 decimal digits */
{
        int bcstat;

        bcstat = ConvertB (sBarcode, 01, 02, BC_START_SYM);

        if (bcstat == BC_OK)
                if (ConvertN (sBarcode, 03, 06, sFCC) != BC_OK)
                        bcstat = BC_INV_FCC;

        if (bcstat == BC_OK)
                if (ConvertN (sBarcode, 07, 22, sSortingCode) != BC_OK)
                        bcstat = BC_INV_SORT_CODE;

        if (bcstat == BC_OK)
                bcstat = ConvertFill (sBarcode, 23, 23);

        if (bcstat == BC_OK)
                bcstat = AppendRSParity (sBarcode, 37);

        if (bcstat == BC_OK)
                bcstat = ConvertB (sBarcode, 36, 37, BC_STOP_SYM);

        return bcstat;
}


/*---------------------------------------------------------------------------
 * BuildBarcode52:
 * Build a length 52 barcode from an FCC, a sorting code and customer info.
 * C encoding is used for the customer info.
 *---------------------------------------------------------------------------*/
int BuildBarcode52(
    char *sBarcode,		/* Output barcode buffe, length >= 53 chars */
    char *sFCC,                 /* Input FCC, 2 decimal digits */
    char *sSortingCode,         /* Input Sorting code, 8 decimal digits */
    char *sCustInfo)            /* Input Cust-info [a-zA-Z0-9 #]. Up to 5 chars */
{
        int bcstat;

        bcstat = ConvertB (sBarcode, 01, 02, BC_START_SYM);

        if (bcstat == BC_OK)
                if (ConvertN (sBarcode, 03, 06, sFCC) != BC_OK)
                        bcstat = BC_INV_FCC;

        if (bcstat == BC_OK)
                if (ConvertN (sBarcode, 07, 22, sSortingCode) != BC_OK)
                        bcstat = BC_INV_SORT_CODE;

        if (bcstat == BC_OK)
                if (ConvertC (sBarcode, 23, 38, sCustInfo) != BC_OK)
                        bcstat = BC_INV_CUST_INFO;

        if (bcstat == BC_OK)
                bcstat = AppendRSParity (sBarcode, 52);

        if (bcstat == BC_OK)
                bcstat = ConvertB (sBarcode, 51, 52, BC_STOP_SYM);

        return bcstat;
}

/*---------------------------------------------------------------------------
 * BuildBarcode67:
 * Build a length 67 barcode from an FCC, a sorting code and customer info.
 * C encoding is used for the customer info.
 *---------------------------------------------------------------------------*/
int BuildBarcode67(
    char *sBarcode,		/* Output barcode buffer, length >= 68 chars */
    char *sFCC,                 /* Input FCC, 2 decimal digits */
    char *sSortingCode,         /* Input Sorting code, 8 decimal digits */
    char *sCustInfo)            /* Input User [a-zA-Z0-9 #]. Up to 10 chars */

{
        int bcstat = BC_OK;

        bcstat = ConvertB (sBarcode, 01, 02, BC_START_SYM);

        if (bcstat == BC_OK)
                if (ConvertN (sBarcode, 03, 06, sFCC) != BC_OK)
                        bcstat = BC_INV_FCC;

        if (bcstat == BC_OK)
                if (ConvertN (sBarcode, 07, 22, sSortingCode) != BC_OK)
                        bcstat = BC_INV_SORT_CODE;

        if (bcstat == BC_OK)
                if (ConvertC (sBarcode,        23, 53, sCustInfo) != BC_OK)
                        bcstat = BC_INV_CUST_INFO;

        if (bcstat == BC_OK)
                bcstat = AppendRSParity (sBarcode, 67);

        if (bcstat == BC_OK)
                bcstat = ConvertB (sBarcode, 66, 67, BC_STOP_SYM);

        return bcstat;
}


/*---------------------------------------------------------------------------
 * BuildBarcode:
 *
 * Build a general purpose barcode. The FCC is validated, and used to determine
 * the barcode type. The sorting info is always encoded. The Customer info is
 * ignored for length 37 barcodes.
 *
 * Input parameters:
 *
 *       Format Control Code   - To be 'N' encoded [0-9]
 *       Sorting Code          - To be 'N' encoded [0-9]
 *       User Info Field       - To be 'C' encoded
 *                               [a-zA-Z0-9 #]
 *
 * Output parameters:
 *
 *       Barcode      - String of barcode digits,
 *                      without null termination.
 *       BarcodeLen   - Length of the barcode
 *
 * Return Codes:
 *
 *       0 - Ok
 *               1 - Invalid Format Control Code
 *               2 - Invalid Sorting Code
 *               3 - Invalid Customer Info Field
 *               4 - Invalid Barcode field range
 *---------------------------------------------------------------------------*/
int BuildBarcode(
    char *sFcc,         /* Format control - 2 decimal digits */
    char *sSortingCode, /* Sorting code - 8 decimal digits */
    char *sCustInfo,    /* Customer info - will be 'C' encoded */
    char *sBarcode,     /* Output barcode */
    int  *iBarcodeLen)  /* Output barcode length */
{
        int bcstat = BC_OK;
	char sTemp[67+1];
	int iLen;

        if (!strncmp(sFcc, FCC_37_CUST, 2)
        ||  !strncmp(sFcc, FCC_37_ROUT, 2)
        ||  !strncmp(sFcc, FCC_37_REPL, 2)
        ||  !strncmp(sFcc, FCC_37_REDI, 2)) {
                bcstat = BuildBarcode37(sTemp, sFcc, sSortingCode);
 		iLen = 37;
        }
        else if (!strncmp(sFcc, FCC_52_FF_MET, 2)) {
                bcstat = BuildBarcode52(sTemp, sFcc, sSortingCode,
                                        sCustInfo);
		iLen = 52;
        }
        else if (!strncmp(sFcc, FCC_67_FF_MET, 2)
             ||  !strncmp(sFcc, FCC_67_FF_MAN, 2)) {

                bcstat = BuildBarcode67(sTemp, sFcc, sSortingCode,
                                        sCustInfo);
		iLen = 67;
        }
        else {
                bcstat = BC_INV_FCC;
        }

	if (bcstat == BC_OK) {
		strncpy(sBarcode, sTemp, iLen);
		*iBarcodeLen = iLen;
	}

        return bcstat;
}

#if BC_DEMO

/*---------------------------------------------------------------------------
 * Main:
 *   Barcode calculator. This routine inputs barcode data from a user,
 *   validates it, and displays a barcode
 *---------------------------------------------------------------------------*/

void main (void)
{
        char sFcc[2+1];
        char sSortingCode[8+1];
        char sCustInfo[20+1];
        char sBarcode[67+1];
        char buf[80+1];
         int iResult;
        int iLength;
        char bc[3][4] = {{'|','|',' ',' '},
                         {'|','|','|','|'},
                         {'|',' ','|',' '}};
        int i,j;
        char cUserRequest;

        printf ("Australia Post Barcode Demo. %s\n\n",
                "ANSI-C version R2,  3rd March 1999.");

        RSInitialise();
        cUserRequest = 'Y';

        while (cUserRequest != 'N' && cUserRequest != 'n') {

                printf ("Please Enter Format Control Code (99) : ");
                fgets(buf, sizeof(buf), stdin);
                sscanf (buf,"%2[^\n]", sFcc);
                printf ("\n");

                printf ("Please Enter Sorting Code (99999999)  : ");
                fgets(buf, sizeof(buf), stdin);
                sscanf (buf, "%8[^\n]", sSortingCode);
                printf ("\n");

                printf ("Please Enter Customer Information     : ");
                fgets(buf, sizeof(buf), stdin);
                sscanf (buf, "%20[^\n]", sCustInfo);
                printf ("\n");

                printf("------------------------------------------------------------------------------\n");
                printf("Format Ctrl Code = '%s'\n", sFcc);
                printf("Sorting Code     = '%s'\n", sSortingCode);
                printf("Customer Info    = '%s'\n", sCustInfo);

                iResult = BuildBarcode(sFcc, sSortingCode, sCustInfo,
				       sBarcode, &iLength);

                printf("Barcode Length   = %d\n", iLength);
                printf("Return Code      = %d (%s)\n", iResult, bcmsg[iResult]);
                if (iResult == BC_OK) {
                        printf("Bar Code:\n");

                        /*
                         * Produce three line character output of the barcode.
                         */

                        for (i = 0; i < 3; i++) {
                            printf("   ");
                            for (j = 0; j < iLength; j++) {
                                printf("%c", bc[i][sBarcode[j] - '0']);
                             }
                             printf ("\n");
                        }
                        printf("   %*.*s\n", iLength, iLength, sBarcode);
                }
            printf ("\n");

	    do {
        	printf ("                       Continue (Y/N) ? ");
		fgets(buf, sizeof(buf), stdin);
		sscanf (buf,"%c", &cUserRequest);
	   } while (strchr ("YyNn", cUserRequest) == NULL);

        }

        return;
}

#endif

