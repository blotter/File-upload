#!/usr/bin/env python
import cgi, os 
import cgitb; cgitb.enable()
import MySQLdb

if __name__ == "__main__":
    message = ''
    form = cgi.FieldStorage()
    conn = MySQLdb.connect(
        host='localhost'
        , user='images'
        , passwd='tNAqQLVH8KZDFKWL'
        , db='images'
    )
    cursor = conn.cursor()
    sql = """
        SELECT
            id_hash
            , origin_name
            , size
            , timestamp
        FROM
            images
        WHERE
            public='1'
        ORDER BY
            timestamp DESC
    """
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    for muh in fetchall:
        if len(str(muh[2])) > 0 and len(str(muh[2])) <= 3:
            _size = '%3s b ' % str(int(muh[2]))
        elif len(str(muh[2])) > 3 and len(str(muh[2])) <= 6:
            _size = '%3s kb' % str(int(muh[2]) / 1024)
        elif len(str(muh[2])) > 6 and len(str(muh[2])) < 9:
            _size = '%3s mb' % str(int(muh[2]) / 1024 / 1024)
        else:
            _size = '%3s byte' % str(int(muh[2]))
        if len(muh[1].rsplit('.',1)[0]) >= 15:
            _name, _extension = muh[1].rsplit('.',1)
            _origin_name = _name[0:8] + '...' + _name[len(_name)-5:] + '.' +  _extension
        else:
            _origin_name = muh[1]

        message += '            <tr>\n'
        message += '                <td class="left">\n'
        message += '<a href="' + muh[0] + '" title="Download ' + muh[1] + '"><img id="small" src="files/download.png" /></a>'
        message += '<a href="' + muh[0] + '-show" title="' + muh[1] + ' Info"><img id="small" src="files/info.png" />' + _origin_name + '</a>\n'
        message += '                </td>\n'
        message += '                <td class="right">\n'
        message += '                    (' + _size.replace(' ', '&nbsp;') + ')\n'
        message += '                </td>\n'
        message += '                <td class="right">\n'
        message += '                    ' + muh[0] + '\n'
        message += '                </td>\n'
        message += '                <td class="right">\n'
        message += '                    ' + str(muh[3]) + '\n'
        message += '                </td>\n'
        message += '            </tr>\n'


    print """\
Content-type: text/html\n
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" dir="ltr" lang="de" xml:lang="de">
    <head>
        <title>www.j4nus.de | images</title>
        <link rel="shortcut icon" href="/favicon.ico" type="image/x-icon" />
        <link rel="stylesheet" type="text/css" href="style.css" />
    </head>
    <body>
        <div class="main">
        <table width="100%">
            <thead>
                <tr>
                    <th>
                        Origin Name
                    </th>
                    <th width="85">
                        File Size
                    </th>
                    <th width="290">
                        MD5hash
                    </th>
                    <th width="171">
                        Upload Date
                    </th>
                </tr>
            </thead>
            <tbody>
            """
    print """\
%s
    """ % (message )
    print """
            </tbody>
        </table>
        </div>
        <div class="footer">
            <form action="save_file.py" method="post" enctype="multipart/form-data">
                <label for="file">
                Filename    :</label>
                <input type="hidden" name="MAX_FILE_SIZE" value="4000000" />
                <input type="file" name="file" id="file" /><br />
                <label for="pulic">
                Public      :</label>
                <input type="radio" name="public" value="1" checked="checked" />yes
                <input type="radio" name="public" value="0" />no<br />
                <input type="submit" name="submit" value="Submit" />
            </form>
        </div>
    </body>
</html>
    """

