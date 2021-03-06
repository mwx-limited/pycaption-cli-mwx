import optparse
import codecs

import pycaption

# dirty hack to set utf-8 as default encoding and fix endless unicode issues
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def main():
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option("--sami",
            action='store_true',
            dest='sami',
            help="write captions in SAMI format",
            default=False,)
    parser.add_option("--dfxp",
            action='store_true',
            dest='dfxp',
            help="write captions in DFXP format",
            default=False,)
    parser.add_option("--srt",
            action='store_true',
            dest='srt',
            help="write captions in SRT format",
            default=False,)
    parser.add_option("--vtt",
            action='store_true',
            dest='webvtt',
            help="write captions in webvtt format",
            default=False,)
    parser.add_option("--transcript",
            action='store_true',
            dest='transcript',
            help="write transcript for captions",
            default=False,)
    parser.add_option("--lang",
            dest='lang',
            help="choose override language for input",
            default='en-US',)
    parser.add_option("--time_offset",
            dest='offset',
            help="choose an offset for input time code; measured in seconds",
            default=0)
    parser.add_option("--use_styling",
            dest='use_styling',
            help="use styling in WebVtt output file or not (True|False)",
            default=True)
    (options, args) = parser.parse_args()

    try:
        filename = args[0]
    except:
        raise Exception(
        ('Expected usage: python caption_converter.py <path to caption file> ',
        '[--sami --dfxp --srt --vtt --use_styling --transcript --lang --time_offset]'))

    captions = ''
    for enc in "utf-8", "utf-8-sig", "utf-16":
        try:
            captions = codecs.open(filename, encoding=str(enc), mode='r').read()
            content = read_captions(captions, options)
            break
        except:
            continue
    if captions != '':
        try:
            write_captions(content, options)
        except Exception,e:
            raise Exception('Error writing file',filename,str(e))
    else:
        raise Exception('Error reading file',filename)

def read_captions(captions, options):
    scc_reader = pycaption.SCCReader()
    srt_reader = pycaption.SRTReader()
    sami_reader = pycaption.SAMIReader()
    dfxp_reader = pycaption.DFXPReader()
    webvtt_reader = pycaption.WebVTTReader()

    if scc_reader.detect(captions):
         return scc_reader.read(captions, lang=options.lang, offset=float(options.offset))
    elif srt_reader.detect(captions):
        return srt_reader.read(captions, lang=options.lang, offset=float(options.offset))
    elif sami_reader.detect(captions):
        return sami_reader.read(captions)
    elif dfxp_reader.detect(captions):
        return dfxp_reader.read(captions)
    elif webvtt_reader.detect(captions):
        return webvtt_reader.read(captions)
    else:
        raise Exception('No caption format detected :(')


def write_captions(content, options):

    if options.sami:
        print pycaption.SAMIWriter().write(content)
    if options.dfxp:
        print pycaption.DFXPWriter().write(content)
    if options.webvtt:
        print pycaption.WebVTTWriter().write(caption_set=content, use_styling=options.use_styling)
    if options.srt:
        print pycaption.SRTWriter().write(content)
    if options.transcript:
        print pycaption.TranscriptWriter().write(content)


if __name__ == '__main__':
    main()
