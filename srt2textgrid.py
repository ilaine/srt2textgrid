from os import path
import argparse
import pysrt

def to_seconds(srt_time):
    return round(
            (srt_time.hours * 3600)\
            + (srt_time.minutes * 60)\
            + srt_time.seconds\
            + (srt_time.milliseconds / 1000),
            2)

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description='Convert SRT file to TextGrid')
    arg_parser.add_argument('-i', '--input', type=str, required=True, help='Path of the Input SRT File')
    arg_parser.add_argument('-o', '--output', type=str, help='Path of the output TextGrid File (default: same as SRT but with .TextGrid extension)')
    
    args = arg_parser.parse_args()
    
    # parse SRT file
    srt = list(filter(
            lambda sub: to_seconds(sub.end) >= to_seconds(sub.start), 
            pysrt.open(args.input)
          ))

    textgrid = None
    if args.output is not None:
        textgrid = open(args.output, "w")
    else:
        input_path_split = path.split(args.input)
        output_path = path.join(input_path_split[0], path.splitext(input_path_split[1])[0] + '.TextGrid') 
        textgrid = open(output_path, "w")

    textgrid.writelines([
        "File type = \"ooTextFile\"\n",
        "Object class = \"TextGrid\"\n\n",
        f"xmin = {to_seconds(srt[0].start)}\n",
        f"xmax = {to_seconds(srt[-1].end)}\n",
        "tiers? <exists>\n",
        "size = 1\n",
        "item []:\n",
        " "*4 + "item [1]:\n",
        " "*8 + "class = \"IntervalTier\"\n",
        " "*8 + "name = \"transcription\"\n",
        " "*8 + f"xmin = {to_seconds(srt[0].start)}\n",
        " "*8 + f"xmax = {to_seconds(srt[-1].end)}\n",
        " "*8 + f"intervals: size = {len(srt)}\n",
    ])
    for index, sub in enumerate(srt):

        clntext = sub.text.replace('\"','\'') # IW: need to replace all "" (used as a text delimitor) by ''
        clntext = clntext.replace('\n','') # IW: need to delete all \n

        if index < len(srt) - 1: # last sentence has different end time
            textgrid.writelines([
                " "*8 + f"intervals [{index + 1}]:\n",
                " "*12 + f"xmin = {to_seconds(sub.start)}\n",
                " "*12 + f"xmax = {round(to_seconds(sub.end) - 0.01, 2)}\n", # subtracting 0.01 produces rounding error
                " "*12 + f"text = \"{clntext}\"\n", # IW: added "" at the beginning and the end of each utterrance
            ])
        else:
            textgrid.writelines([
                " "*8 + f"intervals [{index + 1}]:\n",
                " "*12 + f"xmin = {to_seconds(sub.start)}\n",
                " "*12 + f"xmax = {to_seconds(sub.end)}\n",
                " "*12 + f"text = \"{clntext}\"\n", # IW: added "" at the beginning and the end of each utterrance
            ])

    textgrid.close()
    