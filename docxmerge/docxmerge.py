def docx_run(docx_uri,json_doc,filename):

    import json
    import validators
    import time
    import os
    import re

    current_time = time.time()
    whitelist = "www.example.com" # Sperate domains by semicolons
    location = "" # leave blank
    content = "" # leave blank

    def is_json(myjson):
      try:
        json_object = json.loads(myjson)
      except ValueError:
        return False
      return True

    domain = docx_uri.split("//")[-1].split("/")[0]

    if not docx_uri or not json_doc:

        content = "Error: null value(s)."

    elif is_json(json_doc) and validators.url(docx_uri) and re.search( r'(^|;)'+domain+r'($|;)', whitelist):

        # h/t @vzvenyach https://gist.github.com/vzvenyach/38d1fb78d95f1ae1cfdc#file-docx_mailmerge-py

        import string
        import random
        str = hex(random.getrandbits(20))
        directory = "%s-%s"%(str,int(time.time()))
        # Note: I'm assuming you can write to /var/www/tmp and that this location is a webserver.
        # If either of these assumptions is wrong or if you'd like to drop your files elsewhere, go for it.
        os.mkdir("/var/www/tmp/%s"%directory)
        import urllib.request
        try:
            urllib.request.urlretrieve(docx_uri, "/var/www/tmp/%s/_%s.docx"%(directory,filename))
        except:
            content = "Error: Issue downloading file."

        import zipfile
        import string
        import lxml
        from lxml import etree

        def read_docx(filepath):
            # todo: Add test to make sure it's a docx
            zfile = zipfile.ZipFile(filepath)
            # return the xml
            return zfile.read("word/document.xml")

        def replace_hash(kp, input_string):
            for key, value in kp.items():
                if key in input_string:
                    return value

        def replace_docx(filepath, newfilepath, newfile):
            zin = zipfile.ZipFile(filepath, 'r')
            zout = zipfile.ZipFile(newfilepath, 'w')
            for item in zin.infolist():
                buffer = zin.read(item.filename)
                if (item.filename != 'word/document.xml'):
                    zout.writestr(item, buffer)
                else:
                    zout.writestr('word/document.xml', newfile)
            zin.close()
            zout.close()
            return True

        def check_element_is(element, type_char):
            word_schema = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            return element.tag == '{%s}%s' % (word_schema,type_char)

        def docxmerge(fname, kp, newfname):

            filexml = read_docx(fname)
            my_etree = etree.fromstring(filexml)
            for node in my_etree.iter(tag=etree.Element):

                if check_element_is(node, 'fldChar'): #Once we've hit this, we're money...

                    # Now, we're looking for this attribute: w:fldCharType="separate"con
                    if node.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fldCharType') == "separate":
                        node_value = node.getparent().getnext().getchildren()[1].text
                        node.getparent().getnext().getchildren()[1].text = replace_hash(kp, node_value)

                elif check_element_is(node, 'fldSimple'): #Once we've hit this, we're money...
                    node_value = node.getchildren()[0].getchildren()[1].text
                    node.getchildren()[0].getchildren()[1].text = replace_hash(kp, node_value)

            replace_docx(fname, newfname, etree.tostring(my_etree, encoding='utf8', method='xml'))
            
        if content == "":
            try:
                docxmerge("/var/www/tmp/%s/_%s.docx"%(directory,filename), json.loads(json_doc), "/var/www/tmp/%s/%s.docx"%(directory,filename))
        
                location = "/tmp/%s/%s.docx"%(directory,filename) # Note: this should reference the content's URL
                content = "Wrote something!"
            except:
                content = "Error: Issue parsing file."

    else:

        content = "Error: Invalid input(s)."

    return location, content
