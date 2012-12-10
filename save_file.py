#!/usr/bin/env python
import cgi, os
import cgitb; cgitb.enable()
import hashlib
import shutil
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import mimetypes
import MySQLdb

if __name__ == "__main__":
    form = cgi.FieldStorage()

    # A nested FieldStorage instance holds the file
    fileitem = form['file']

    # Test if the file was uploaded
    if fileitem.filename:
        message = '<tbody>'
        _filedata =''
        conn = MySQLdb.connect(
            host='localhost'
           , user='images'
           , passwd='tNAqQLVH8KZDFKWL'
           , db='images'
        )
        cursor = conn.cursor()

    
        # strip leading path from file name to avoid directory traversal attacks
        _fn = os.path.basename(fileitem.filename)
        _file = fileitem.file
        _hash = hashlib.md5()
    
        while True:
            _data = _file.read(8192)
            _filedata += _data
            if not _data:
                break
            _hash.update(_data)

        _md5 = _hash.hexdigest()

        open('/tmp/' + _fn, 'wb').write(_filedata)

        _mime = mimetypes.guess_type('/tmp/' + _fn)
        _size = os.path.getsize('/tmp/' + _fn)
        if _mime[0] == None:
            _content_type = 'None'
        else:
            _content_type = _mime[0]

        try:
            os.remove('/tmp/' + _fn)
        except:
            message += '<tr>\n'
            message += '<td>Error: </td>\n'
            message += '<td>delete "/tmp/' + _fn + '" failed</td>\n'
            message += '</tr>\n'
        else:
            message += '<tr>\n'
            message += '<td>Delete: </td>\n'
            message += '<td>Done!</td>\n'
            message += '</tr>\n'

        try:
            _selectDB = (_md5)
            sql = "SELECT id_hash FROM images WHERE id_hash=%s"
            cursor.execute(sql, _selectDB)
            fetchall = cursor.fetchall()[0]

        except IndexError:
            message += '<tr>\n'
            message += '<td>MySQL: </td>\n'
            message += '<td>Hash ' + _md5 + ' not found!</td>\n'
            message += '</tr>\n'

            try:
                _insertDB = (_md5, form['public'].value , _fn, _content_type, str(_size), _filedata)
                sql = "INSERT INTO images (id_hash, public, origin_name, content_type, size, binary_data) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, _insertDB)
                conn.commit()
                cursor.close()

            except:
                message += '<tr>\n'
                message += '<td>Error: </td>\n'
                message += '<td>Fehler beim MySQL INSERT</td>\n'
                message += '</tr>\n'
            else:
                if str(form['public'].value) == "1":
                    _show_public = "yes"
                else:
                    _show_public = "no"

                message += '<tr>\n'
                message += '<td>MySQL: </td>\n'
                message += '<td>erfolgreich!</td>\n'
                message += '</tr>\n'
                message += '<tr>\n'
                message += '<td>md5: </td>\n'
                message += '<td>' + _md5 + '</td>\n'
                message += '</tr>\n'
                message += '<tr>\n'
                message += '<td>Name: </td>\n'
                message += '<td>' + _fn + '</td>\n'
                message += '</tr>\n'
                message += '<tr>\n'
                message += '<td>ContentType: </td>\n'
                message += '<td>' + _content_type + '</td>\n'
                message += '</tr>\n'
                message += '<tr>\n'
                message += '<td>Size: </td>\n'
                message += '<td>' + str(_size) + '</td>\n'
                message += '</tr>\n'
                message += '<tr>\n'
                message += '<td>Public: </td>\n'
                message += '<td>' + _show_public + '</td>\n'
                message += '</tr>\n'
        else:
            message += '<tr>\n'
            message += '<td>Error: </td>\n'
            message += '<td>Hash ' + _md5 + ' exists!</td>\n'
            message += '</tr>\n'

        message += '</tbody>\n</table>\n<br />\n'
        if _content_type.split('/')[0] == "image":
            _data = '<a href="%s-show"><img src="%s" /></a>\n' % (_md5, _md5)
        elif _content_type.split('/')[0] == "text" or _content_type.split('/')[0] == "application":
            _data = '<div class="highlieht">' + highlight(_filedata, PythonLexer(), HtmlFormatter()) + '</div>\n'
        else:
            _data = '<a href="%s-show">%s</a>\n' % (_md5, _md5)
        
        message += _data
    else:
        message = 'No file was uploaded'


    print """\
Content-Type: text/html\n
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="de" xml:lang="de">
    <head>
        <title>www.j4nus.de | images</title>
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <link rel="stylesheet" type="text/css" href="style.css"/>
        <link rel="stylesheet" type="text/css" href="highlight.css"/>
    </head>
    <body>
        <div class="left">
            <div>
                [ <a href=".">Index</a> ]
                [ <a href="%s">Download</a> ]
                [ <a href="%s-show">Info</a> ]
            </div>
            <br />
            <div>
                <table width="600">
                    <thead>
                        <tr>
                            <th>Var</th>
                            <th>Value</th>
                       </tr>
                    </thead>
%s
    </body>
</html>
    """ % (_md5, _md5, message,)
