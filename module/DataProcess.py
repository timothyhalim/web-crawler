import re
import zlib, base64 

class DataProcess():
    @staticmethod
    def make_file_friendly_name(text):
        return str("").join([x for x in text if x not in "\\/:?|<>"])

    @staticmethod
    def fix_bracket(s):
        for e in ["em", "strong"]:
            s = re.sub(r"(\S)<"+e+r">", r"\1 <"+e+r">", s) # add space before <{e}>
            s = re.sub(r"<"+e+r">\s+(\S)", r"<"+e+r">\1", s) # remove space after <{e}>
            s = re.sub(r"(\S)\s+</"+e+r">", r"\1</"+e+r">", s) # remove space before <\{e}>
            s = re.sub(r"</"+e+r">(\S)", r"</"+e+r"> \1", s) # add space after <\{e}>
        
        s = re.sub("<em>", "*", s) # make italic
        s = re.sub("</em>", "*", s) # make italic
        s = re.sub("<strong>", " **", s) # make bold
        s = re.sub("</strong>", "** ", s) # make bold
        
        s = re.sub("<.+=\".+?\">", "", s) # Remove <x x="blabla">
        s = re.sub("<sup>.+</sup>", "", s) # Remove superscript
        s = re.sub("<sub>.+</sub>", "", s) # Remove subscript
        s = re.sub("</.+>", "", s) # Remove </blbabla>
        s = re.sub("=\"\"", "", s) # Remove =""
        
        s = re.sub("<", "&lt;", s) # Make < web friendly
        s = re.sub(">", "&gt;", s) # Make > web friendly
        
        s = re.sub(r'(\*{2})(.*?)(\*{2})', r"<strong>\2</strong>", s)
        s = re.sub(r'(\*{1})(.*?)(\*{1})', r"<em>\2</em>", s)
        
        s = f"<p>{s}</p>"
        
        return s

    @staticmethod
    def encode_text(text):
        code =  base64.b64encode(zlib.compress(text.encode('utf-8'),9)) 
        code = code.decode('utf-8') 
        return code

    @staticmethod
    def decode_text(text):
        decoded_txt = zlib.decompress(base64.b64decode(text)) 
        return (decoded_txt) 

    @staticmethod
    def atof(text):
        try:
            retval = float(text)
        except ValueError:
            retval = text
        return retval

    @staticmethod
    def natural_keys(text):
        '''
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        float regex comes from https://stackoverflow.com/a/12643073/190597
        '''
        return [ DataProcess.atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]