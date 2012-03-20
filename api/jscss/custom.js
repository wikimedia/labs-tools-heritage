// Global external objects used by this script.
/*extern ta, stylepath, skin */

// add any onload functions in this hook (please don't hard-code any events in the xhtml source)
var doneOnloadHook;

if (!window.onloadFuncts) {
        var onloadFuncts = [];
}

function addOnloadHook( hookFunct ) {
        // Allows add-on scripts to add onload functions
        if( !doneOnloadHook ) {
                onloadFuncts[onloadFuncts.length] = hookFunct;
        } else {
                hookFunct();  // bug in MSIE script loading
        }
}

function hookEvent( hookName, hookFunct ) {
        addHandler( window, hookName, hookFunct );
}

function runOnloadHook() {
        // don't run anything below this for non-dom browsers
        if ( doneOnloadHook || !( document.getElementById && document.getElementsByTagName ) ) {
                return;
        }

        // set this before running any hooks, since any errors below
        // might cause the function to terminate prematurely
        doneOnloadHook = true;

        sortables_init();

        // Run any added-on functions
        for ( var i = 0; i < onloadFuncts.length; i++ ) {
                onloadFuncts[i]();
        }
}

/**
 * Add an event handler to an element
 *
 * @param Element element Element to add handler to
 * @param String attach Event to attach to
 * @param callable handler Event handler callback
 */
function addHandler( element, attach, handler ) {
        if( window.addEventListener ) {
                element.addEventListener( attach, handler, false );
        } else if( window.attachEvent ) {
                element.attachEvent( 'on' + attach, handler );
        }
}




/*
        Written by Jonathan Snook, http://www.snook.ca/jonathan
        Add-ons by Robert Nyman, http://www.robertnyman.com
        Author says "The credit comment is all it takes, no license. Go crazy with it!:-)"
        From http://www.robertnyman.com/2005/11/07/the-ultimate-getelementsbyclassname/
*/
function getElementsByClassName( oElm, strTagName, oClassNames ) {
        var arrReturnElements = new Array();
        if ( typeof( oElm.getElementsByClassName ) == 'function' ) {
                /* Use a native implementation where possible FF3, Saf3.2, Opera 9.5 */
                var arrNativeReturn = oElm.getElementsByClassName( oClassNames );
                if ( strTagName == '*' ) {
                        return arrNativeReturn;
                }
                for ( var h = 0; h < arrNativeReturn.length; h++ ) {
                        if( arrNativeReturn[h].tagName.toLowerCase() == strTagName.toLowerCase() ) {
                                arrReturnElements[arrReturnElements.length] = arrNativeReturn[h];
                        }
                }
                return arrReturnElements;
        }
        var arrElements = ( strTagName == '*' && oElm.all ) ? oElm.all : oElm.getElementsByTagName( strTagName );
        var arrRegExpClassNames = new Array();
        if( typeof oClassNames == 'object' ) {
                for( var i = 0; i < oClassNames.length; i++ ) {
                        arrRegExpClassNames[arrRegExpClassNames.length] =
                                new RegExp("(^|\\s)" + oClassNames[i].replace(/\-/g, "\\-") + "(\\s|$)");
                }
        } else {
                arrRegExpClassNames[arrRegExpClassNames.length] =
                        new RegExp("(^|\\s)" + oClassNames.replace(/\-/g, "\\-") + "(\\s|$)");
        }
        var oElement;
        var bMatchesAll;
        for( var j = 0; j < arrElements.length; j++ ) {
                oElement = arrElements[j];
                bMatchesAll = true;
                for( var k = 0; k < arrRegExpClassNames.length; k++ ) {
                        if( !arrRegExpClassNames[k].test( oElement.className ) ) {
                                bMatchesAll = false;
                                break;
                        }
                }
                if( bMatchesAll ) {
                        arrReturnElements[arrReturnElements.length] = oElement;
                }
        }
        return ( arrReturnElements );
}

/* ************************ */
function getInnerText( el ) {
        if ( typeof el == 'string' ) {
                return el;
        }
        if ( typeof el == 'undefined' ) {
                return el;
        }
        if ( el.textContent ) {
                return el.textContent; // not needed but it is faster
        }
        if ( el.innerText ) {
                return el.innerText; // IE doesn't have textContent
        }
        var str = '';

        var cs = el.childNodes;
        var l = cs.length;
        for ( var i = 0; i < l; i++ ) {
                switch ( cs[i].nodeType ) {
                        case 1: // ELEMENT_NODE
                                str += ts_getInnerText( cs[i] );
                                break;
                        case 3: // TEXT_NODE
                                str += cs[i].nodeValue;
                                break;
                }
        }
        return str;
}


/*
 * Table sorting script based on one (c) 1997-2006 Stuart Langridge and Joost
 * de Valk:
 * http://www.joostdevalk.nl/code/sortable-table/
 * http://www.kryogenix.org/code/browser/sorttable/
 *
 * @todo don't break on colspans/rowspans (bug 8028)
 * @todo language-specific digit grouping/decimals (bug 8063)
 * @todo support all accepted date formats (bug 8226)
 */

var ts_image_path = 'http://toolserver.org/~erfgoed/toolbox/img/';
var ts_image_up = 'Sort_up.gif';
var ts_image_down = 'Sort_down.gif';
var ts_image_none = 'Sort_none.gif';
var ts_europeandate = true; // The non-American-inclined can change to "true"
var ts_alternate_row_colors = false;
var ts_number_transform_table = null;
var ts_number_regex = null;

function sortables_init() {
        var idnum = 0;
        // Find all tables with class sortable and make them sortable
        var tables = getElementsByClassName( document, 'table', 'sortable' );
        for ( var ti = 0; ti < tables.length ; ti++ ) {
                if ( !tables[ti].id ) {
                        tables[ti].setAttribute( 'id', 'sortable_table_id_' + idnum );
                        ++idnum;
                }
                ts_makeSortable( tables[ti] );
        }
}
function ts_makeSortable( table ) {
        var firstRow;
        if ( table.rows && table.rows.length > 0 ) {
                if ( table.tHead && table.tHead.rows.length > 0 ) {
                        firstRow = table.tHead.rows[table.tHead.rows.length-1];
                } else {
                        firstRow = table.rows[0];
                }
        }
        if ( !firstRow ) {
                return;
        }


        // We have a first row: assume it's the header, and make its contents clickable links
        for ( var i = 0; i < firstRow.cells.length; i++ ) {
                var cell = firstRow.cells[i];
                if ( (' ' + cell.className + ' ').indexOf(' unsortable ') == -1 ) {
                        cell.innerHTML += '<a href="#" class="sortheader" '
                                + 'onclick="ts_resortTable(this);return false;">'
                                + '<span class="sortarrow">'
                                + '<img src="'
                                + ts_image_path
                                + ts_image_none
                                + '" alt="&darr;"/></span></a>';
                }
        }
        if ( ts_alternate_row_colors ) {
                ts_alternate( table );
        }
}

function ts_getInnerText( el ) {
        return getInnerText( el );
}
function ts_resortTable( lnk ) {
        // get the span
        var span = lnk.getElementsByTagName('span')[0];

        var td = lnk.parentNode;
        var tr = td.parentNode;
        var column = td.cellIndex;

        var table = tr.parentNode;
        while ( table && !( table.tagName && table.tagName.toLowerCase() == 'table' ) ) {
                table = table.parentNode;
        }
        if ( !table ) {
                return;
        }

        if ( table.rows.length <= 1 ) {
                return;
        }

        // Generate the number transform table if it's not done already
        if ( ts_number_transform_table === null ) {
                ts_initTransformTable();
        }
        // Work out a type for the column
        // Skip the first row if that's where the headings are
        var rowStart = ( table.tHead && table.tHead.rows.length > 0 ? 0 : 1 );

        var itm = '';
        for ( var i = rowStart; i < table.rows.length; i++ ) {
                if ( table.rows[i].cells.length > column ) {
                        itm = ts_getInnerText(table.rows[i].cells[column]);
                        itm = itm.replace(/^[\s\xa0]+/, '').replace(/[\s\xa0]+$/, '');
                        if ( itm != '' ) {
                                break;
                        }
                }
        }

        // TODO: bug 8226, localised date formats
        var sortfn = ts_sort_generic;
        var preprocessor = ts_toLowerCase;
        if ( /^\d\d[\/. -][a-zA-Z]{3}[\/. -]\d\d\d\d$/.test( itm ) ) {
                preprocessor = ts_dateToSortKey;
        } else if ( /^\d\d[\/.-]\d\d[\/.-]\d\d\d\d$/.test( itm ) ) {
                preprocessor = ts_dateToSortKey;
        } else if ( /^\d\d[\/.-]\d\d[\/.-]\d\d$/.test( itm ) ) {
                preprocessor = ts_dateToSortKey;
                // (minus sign)([pound dollar euro yen currency]|cents)
        } else if ( /(^([-\u2212] *)?[\u00a3$\u20ac\u00a4\u00a5]|\u00a2$)/.test( itm ) ) {
                preprocessor = ts_currencyToSortKey;
        } else if ( ts_number_regex.test( itm ) ) {
                preprocessor = ts_parseFloat;
        }

        var reverse = ( span.getAttribute( 'sortdir' ) == 'down' );

        var newRows = new Array();
        var staticRows = new Array();
        for ( var j = rowStart; j < table.rows.length; j++ ) {
                var row = table.rows[j];
                if( (' ' + row.className + ' ').indexOf(' unsortable ') < 0 ) {
                        var keyText = ts_getInnerText( row.cells[column] );
                        if( keyText === undefined ) {
                                keyText = '';
                        }
                        var oldIndex = ( reverse ? -j : j );
                        var preprocessed = preprocessor( keyText.replace(/^[\s\xa0]+/, '').replace(/[\s\xa0]+$/, '') );

                        newRows[newRows.length] = new Array( row, preprocessed, oldIndex );
                } else {
                        staticRows[staticRows.length] = new Array( row, false, j-rowStart );
                }
        }

        newRows.sort( sortfn );

        var arrowHTML;
        if ( reverse ) {
                arrowHTML = '<img src="' + ts_image_path + ts_image_down + '" alt="&darr;"/>';
                newRows.reverse();
                span.setAttribute( 'sortdir', 'up' );
        } else {
                arrowHTML = '<img src="' + ts_image_path + ts_image_up + '" alt="&uarr;"/>';
                span.setAttribute( 'sortdir', 'down' );
        }

        for ( var i = 0; i < staticRows.length; i++ ) {
                var row = staticRows[i];
                newRows.splice( row[2], 0, row );
        }
        // We appendChild rows that already exist to the tbody, so it moves them rather than creating new ones
        // don't do sortbottom rows
        for ( var i = 0; i < newRows.length; i++ ) {
                if ( ( ' ' + newRows[i][0].className + ' ').indexOf(' sortbottom ') == -1 ) {
                        table.tBodies[0].appendChild( newRows[i][0] );
                }
        }
        // do sortbottom rows only
        for ( var i = 0; i < newRows.length; i++ ) {
                if ( ( ' ' + newRows[i][0].className + ' ').indexOf(' sortbottom ') != -1 ) {
                        table.tBodies[0].appendChild( newRows[i][0] );
                }
        }

        // Delete any other arrows there may be showing
        var spans = getElementsByClassName( tr, 'span', 'sortarrow' );
        for ( var i = 0; i < spans.length; i++ ) {
                spans[i].innerHTML = '<img src="' + ts_image_path + ts_image_none + '" alt="&darr;"/>';
        }
        span.innerHTML = arrowHTML;

        if ( ts_alternate_row_colors ) {
                ts_alternate( table );
        }
}
function ts_initTransformTable() {
        if ( typeof wgSeparatorTransformTable == 'undefined'
                        || ( wgSeparatorTransformTable[0] == '' && wgDigitTransformTable[2] == '' ) )
        {
                digitClass = "[0-9,.]";
                ts_number_transform_table = false;
        } else {
                ts_number_transform_table = {};
                // Unpack the transform table
                // Separators
                ascii = wgSeparatorTransformTable[0].split("\t");
                localised = wgSeparatorTransformTable[1].split("\t");
                for ( var i = 0; i < ascii.length; i++ ) {
                        ts_number_transform_table[localised[i]] = ascii[i];
                }
                // Digits
                ascii = wgDigitTransformTable[0].split("\t");
                localised = wgDigitTransformTable[1].split("\t");
                for ( var i = 0; i < ascii.length; i++ ) {
                        ts_number_transform_table[localised[i]] = ascii[i];
                }

                // Construct regex for number identification
                digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', '\\.'];
                maxDigitLength = 1;
                for ( var digit in ts_number_transform_table ) {
                        // Escape regex metacharacters
                        digits.push(
                                digit.replace( /[\\\\$\*\+\?\.\(\)\|\{\}\[\]\-]/,
                                        function( s ) { return '\\' + s; } )
                        );
                        if ( digit.length > maxDigitLength ) {
                                maxDigitLength = digit.length;
                        }
                }
                if ( maxDigitLength > 1 ) {
                        digitClass = '[' + digits.join( '', digits ) + ']';
                } else {
                        digitClass = '(' + digits.join( '|', digits ) + ')';
                }
        }

        // We allow a trailing percent sign, which we just strip.  This works fine
        // if percents and regular numbers aren't being mixed.
        ts_number_regex = new RegExp(
                "^(" +
                        "[-+\u2212]?[0-9][0-9,]*(\\.[0-9,]*)?(E[-+\u2212]?[0-9][0-9,]*)?" + // Fortran-style scientific
                        "|" +
                        "[-+\u2212]?" + digitClass + "+%?" + // Generic localised
                ")$", "i"
        );
}
function ts_toLowerCase( s ) {
        return s.toLowerCase();
}

function ts_dateToSortKey( date ) {
        // y2k notes: two digit years less than 50 are treated as 20XX, greater than 50 are treated as 19XX
        if ( date.length == 11 ) {
                switch ( date.substr( 3, 3 ).toLowerCase() ) {
                        case 'jan':
                                var month = '01';
                                break;
                        case 'feb':
                                var month = '02';
                                break;
                        case 'mar':
                                var month = '03';
                                break;
                        case 'apr':
                                var month = '04';
                                break;
                        case 'may':
                                var month = '05';
                                break;
                        case 'jun':
                                var month = '06';
                                break;
                        case 'jul':
                                var month = '07';
                                break;
                        case 'aug':
                                var month = '08';
                                break;
                        case 'sep':
                                var month = '09';
                                break;
                        case 'oct':
                                var month = '10';
                                break;
                        case 'nov':
                                var month = '11';
                                break;
                        case 'dec':
                                var month = '12';
                                break;
                        // default: var month = '00';
                }
                return date.substr( 7, 4 ) + month + date.substr( 0, 2 );
        } else if ( date.length == 10 ) {
                if ( ts_europeandate == false ) {
                        return date.substr( 6, 4 ) + date.substr( 0, 2 ) + date.substr( 3, 2 );
                } else {
                        return date.substr( 6, 4 ) + date.substr( 3, 2 ) + date.substr( 0, 2 );
                }
        } else if ( date.length == 8 ) {
                yr = date.substr( 6, 2 );
                if ( parseInt( yr ) < 50 ) {
                        yr = '20' + yr;
                } else {
                        yr = '19' + yr;
                }
                if ( ts_europeandate == true ) {
                        return yr + date.substr( 3, 2 ) + date.substr( 0, 2 );
                } else {
                        return yr + date.substr( 0, 2 ) + date.substr( 3, 2 );
                }
        }
        return '00000000';
}

function ts_parseFloat( s ) {
        if ( !s ) {
                return 0;
        }
        if ( ts_number_transform_table != false ) {
                var newNum = '', c;

                for ( var p = 0; p < s.length; p++ ) {
                        c = s.charAt( p );
                        if ( c in ts_number_transform_table ) {
                                newNum += ts_number_transform_table[c];
                        } else {
                                newNum += c;
                        }
                }
                s = newNum;
        }
        num = parseFloat( s.replace(/[, ]/g, '').replace("\u2212", '-') );
        return ( isNaN( num ) ? -Infinity : num );
}

function ts_currencyToSortKey( s ) {
        return ts_parseFloat(s.replace(/[^-\u22120-9.,]/g,''));
}
function ts_sort_generic( a, b ) {
        return a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : a[2] - b[2];
}

function ts_alternate( table ) {
        // Take object table and get all it's tbodies.
        var tableBodies = table.getElementsByTagName( 'tbody' );
        // Loop through these tbodies
        for ( var i = 0; i < tableBodies.length; i++ ) {
                // Take the tbody, and get all it's rows
                var tableRows = tableBodies[i].getElementsByTagName( 'tr' );
                // Loop through these rows
                // Start at 1 because we want to leave the heading row untouched
                for ( var j = 0; j < tableRows.length; j++ ) {
                        // Check if j is even, and apply classes for both possible results
                        var oldClasses = tableRows[j].className.split(' ');
                        var newClassName = '';
                        for ( var k = 0; k < oldClasses.length; k++ ) {
                                if ( oldClasses[k] != '' && oldClasses[k] != 'even' && oldClasses[k] != 'odd' ) {
                                        newClassName += oldClasses[k] + ' ';
                                }
                        }
                        tableRows[j].className = newClassName + ( j % 2 == 0 ? 'even' : 'odd' );
                }
        }
}

/*
 * End of table sorting code
 */









// note: all skins should call runOnloadHook() at the end of html output,
//      so the below should be redundant. It's there just in case.
hookEvent( 'load', runOnloadHook );

