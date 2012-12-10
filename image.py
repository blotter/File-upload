#!/usr/bin/env python
import MySQLdb
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
import ConfigParser
import cgi, os 
import cgitb; cgitb.enable()

def main():
    try:
        action = form['action'].value
    except:
        try:
            sql = 'SELECT content_type, binary_data FROM images WHERE id_hash = %s'
            cursor.execute(sql, form['filename'].value)
            _contentType, _filedata = cursor.fetchall()[0]
        except:
            print "Content-type: text/html\n"
            print """
<html>
    <body>
        <p>
            Das Bild existiert nicht! ;)
        </p>
    </body>
</html>
            """

        else:
            print "Content-type: " + _contentType + "\n"
            print _filedata
    else:
        try:
            sql = 'SELECT id_hash, origin_name, content_type, size, timestamp, binary_data, public FROM images WHERE id_hash = %s'
            cursor.execute(sql, form['filename'].value)
            _id_hash, _origin_name, _content_type, _size, _timestamp, _binary_data, _public = cursor.fetchall()[0]
        except:
            print "Content-type: text/html\n"
            print """
<html>
    <body>
        <p>
            Das Bild existiert nicht! ;)
        </p>
    </body>
</html>
            """
        else:
            if str(_public) == "1":
                _public_show = "yes"
            else:
                _public_show = "no"
            if _content_type.split('/')[0] == "image":
                _data = '<div class="highlight center"><br /><a href="%s"><img src="%s" /></a><br /><br /></div>' % (_id_hash, _id_hash)
            elif _content_type.split('/')[0] == "text" or _content_type.split('/')[0] == "application" :
                _data = highlight(_binary_data, PythonLexer(), HtmlFormatter())
            else:
                _data = '<div><a href="%s">%s</a></div>' % (_id_hash, _origin_name)
            print "Content-type: text/html\n"
            print """
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
                [ <a href="./">Index</a> ] 
                [ <a href="%s">Download</a> ]
            </div>
            <br />
            <div>
                <table width="490">
                    <thead>
                        <tr width="150">
                            <th>Var</th>
                            <th>Value</th>
                        <tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>md5: </td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>Name: </td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>ContentType: </td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>Size: </td>
                            <td>%s byte</td>
                        </tr>
                        <tr>
                            <td>Create: </td>
                            <td>%s</td>
                        </tr>
                        <tr>
                            <td>Public: </td>
                            <td>%s</td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <br />
            """ % (_id_hash, _id_hash, _origin_name, _content_type, _size, _timestamp, _public_show)
            print """
            %s
        </div>
    </body>
</html>
            """ % (_data)
if __name__ == "__main__":
    error = ''
    config = ConfigParser.RawConfigParser()
    #try:
    config.read('config.inc')
    try:
        hostname = config.get('mySQLd', 'host')
        username = config.get('mySQLd', 'user')
        password = config.get('mySQLd', 'passwd')
        database = config.get('mySQLd', 'db')
    except ConfigParser.NoSectionError:
        error += 'ConfigParser: No Section found\n'
    except ConfigParser.NoOptionError:
        error += 'ConfigParser: No Option found\n'
    form = cgi.FieldStorage()
    try:
        conn = MySQLdb.connect(
            host = hostname
            , user = username
            , passwd = password
            , db = database
        )
        cursor = conn.cursor()
    except MySQLdb.OperationalError:
        error += 'MySQLdb: Connect Error\n'
    
    if error != '':
        print "Content-type: text/html\n"
        print """ 
<html>
    <body>
        <div>
           %s 
        </div>
    </body>
</html>
        """ % (error,)
    else:
        main()
