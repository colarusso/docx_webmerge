# docx_webmerge
Use JSON to populate a .docx file via a form submit. Here is a [live example](http://www.qnamarkup.org/docxmerge/). This tool is pretty much [Dave Zvenyach](https://gist.github.com/vzvenyach)'s `docx_mailmerge.py` as a webservice. You can find the original code in his post [Mailmerge for Word Docs... in Python?](https://esq.io/blog/posts/python-docx-mailmerge/)

## How To

Assuming you have this repo's Python app up and running on a server, all one has to do is: 

1. Create a .docx Word document with mailmerge feilds; 
2. Upload your document to a webserver hosted on a whitelisted domain (defined in `docxmerge/docxmerge.py`); and 
3. [Pass](http://www.qnamarkup.org/docxmerge/) the document's location (docx_uri), your desired filename (name), and some JSON data (json_doc) to the service.

After that, the service will return a .docx document populated with your JSON data.

Note: if you're a non-profit and would like me to add your website to the whitelist for the example service available at [http://colarusso.pythonanywhere.com/](http://colarusso.pythonanywhere.com/) (the app behind the [live example](http://www.qnamarkup.org/docxmerge/) linked above), let me know. As long as you aren't expecting wicked crazy volume, I'll probably just add you to the list.

## Known Issues

Check out this repo's [Issues tab](https://github.com/colarusso/docx_webmerge/issues) for a list of known issues. 
