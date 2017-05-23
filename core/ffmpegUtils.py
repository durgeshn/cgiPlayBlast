""" FFMPEG dedicated module, to manipulate videos."""

# Import
import os
import struct

FFMPEG_PATH = '//stor/Data/python_packages/tools/ffmpeg/bin/ffmpeg'


def make_path(path, suffix):
    tmp = os.path.splitext(path)
    return '%s_%s%s' % (tmp[0], suffix, tmp[1])


def extract_audio_from_mov(src_mov, dst_audio=None):
    """
    Extract the audio WAV track from a given MOV file. If destination path is not provided it will be extrapolated from
    movie file path.

    :param src_mov: the path to the source MOV file.
    :type src_mov: str
    :param dst_audio: (optional) the path to the destination WAV file.
    :type dst_audio: str
    :return: result of the creation process (True if ok)
    :rtype: bool
    """
    # Extrapolate dst_audio from src_mov if None
    if not dst_audio:
        dst_audio = src_mov.replace('.mov', '.wav')

    # Init cmd
    cmd = r' '.join((FFMPEG_PATH,
                     '-i',
                     str(src_mov),
                     '-acodec',
                     'pcm_s16le',
                     '-ac',
                     '2',
                     str(dst_audio)))

    # Extract!
    res = os.system(cmd)

    # Result will be ok if equal to 0
    res = True if res == 0 else False

    return res


def create_video_from_tif(src_file_pattern, dest_filename, extra_mov_path='', cut_in=101, vcodec='dnxhd', framerate=25):
    """
    ATTENTION LE CODEC CHANGE EN FONCTION DU FPS
    25 -> 185M
    24 -> 175M
    ETC

    :param src_file_pattern:
    :param dest_filename:
    :param extra_mov_path:
    :param cut_in:
    :param vcodec:
    :param framerate:
    :return:
    """
    cmd = None
    try:
        # Define creation command
        cmd = r' '.join((FFMPEG_PATH,
                         r'-start_number', str(cut_in),
                         r'-i', str(src_file_pattern),  # input files
                         r'-framerate', str(framerate),  # set framerate
                         r'-vcodec', vcodec,  # codec
                         r'-b:v', r'185M',
                         r'-f', r'mov',  # force output format
                         r'-y',  # overwrite
                         str(dest_filename)))
        # Make it!
        os.system(cmd)

        # Duplicate file if needed
        if extra_mov_path:
            extra_cmd = r' '.join(('copy',
                                   str(dest_filename),
                                   str(extra_mov_path)))
            os.system(extra_cmd)

    except:
        print cmd
        raise ValueError(('ERROR : could not create video :', dest_filename))

    if os.path.exists(dest_filename):
        return 1
    else:
        return 0


def compare_videos_with_overlay(bg_video, fg_video, output_path):
    """
    Compare two videos by overlaying them with an alpha value of 0.75.

    The resulting video is placed in output_path if this parameter is given, else it will be placed in the same 
    directory as bg_video.

    :param bg_video: the first video to compare (background).
    :type bg_video: string
    :param fg_video: the second video to compare (foreground).
    :type fg_video: string
    :param output_path: (optional) the path of the output video.
    :type output_path: string
    :return: the output_path.
    :rtype: string
    """
    # Init
    suffix = 'compare'
    output_path = make_path(output_path, suffix)
    # FFMPEG command
    cmd = r' '.join((FFMPEG_PATH,
                     r'-i', bg_video,
                     r'-i', fg_video,
                     r'-filter_complex "[0:v]setpts=PTS-STARTPTS[fg]; '
                     r'[fg][1:v]blend=all_mode=\'overlay\':all_opacity=0.75[out]"',
                     r'-map [out] -map 0:a ',
                     output_path))
    # Run!
    os.system(cmd)

    return output_path


def compare_videos_with_difference(bg_video, fg_video, output_path=''):
    """
    Compare two videos by checking differences between them.

    The resulting video is placed in output_path if this parameter is given, else it will be placed in the same 
    directory as bg_video.

    :param bg_video: the first video to compare (background).
    :type bg_video: string
    :param fg_video: the second video to compare (foreground).
    :type fg_video: string
    :param output_path: (optional) the path of the output video.
    :type output_path: string
    :return: the output_path.
    :rtype: string
    """
    # Init
    suffix = 'difference'
    output_path = make_path(output_path, suffix)

    # FFMPEG command
    cmd = r' '.join((FFMPEG_PATH,
                     r'-i', bg_video,
                     r'-i', fg_video,
                     r'-filter_complex "[0:v]setpts=PTS-STARTPTS[fg]; [fg][1:v]blend=all_mode=difference[out]"',
                     r'-map [out] -map 0:a ',
                     output_path))
    # Run!
    os.system(cmd)

    return output_path


def compare_videos_side_by_side(bg_video, fg_video, output_path=''):
    """
    Compare two videos side by side.

    The resulting video is placed in output_path if this parameter is given, else it will be placed in the same 
    directory as bg_video.

    :param bg_video: the first video to compare (background).
    :type bg_video: string
    :param fg_video: the second video to compare (foreground).
    :type fg_video: string
    :param output_path: (optional) the path of the output video.
    :type output_path: string
    :return: the output_path.
    :rtype: string
    """
    # Init
    suffix = 'panels'
    output_path = make_path(output_path, suffix)

    # FFMPEG command
    cmd = r' '.join((FFMPEG_PATH,
                     r'-i', bg_video,
                     r'-i', fg_video,
                     r'-filter_complex "[0:v]setpts=PTS-STARTPTS, pad=iw*2:ih[bg]; '
                     r'[1:v]setpts=PTS-STARTPTS[fg]; '
                     r'[bg][fg]overlay=w; '
                     r'amerge,pan=stereo:c0<c0+c2:c1<c1+c3"',
                     output_path))
    # Run!
    os.system(cmd)

    return output_path


##########
# IMAGES #
##########
def hd_to_ld(hd_path, ld_size=None, ffmpeg_dir=None):
    """
    Here we write Low def of a png in the same folder

    We using ffmpeg

    :param hd_path: 'string' : source image path
    :param ld_size: int or list[int] :
    int -> [int,int]
    [int1, int2, int3] -> [int1, int2]
    other -> default_list[old ize x/5, old ize y/5]
    :param ffmpeg_dir: ffmpeg.exe directory path
    default = path_maker()['ffmpeg_dir']
    """

    # we get path to ffmpeg.exe for Yakari
    if not ffmpeg_dir:
        ffmpeg_dir = FFMPEG_PATH
    else:
        ffmpeg_dir = os.path.join(ffmpeg_dir, 'ffmpeg')

    # Here we set ld_size
    if type(ld_size) is list:
        if len(ld_size) >= 2:
            ld_size = ld_size[0:2]
        elif ld_size:
            ld_size.append(ld_size)
    elif type(ld_size) is int:
        ld_size = [ld_size, ld_size]
    else:  # if no or wrong ld_size was given, we create the default LD size base on the size of the source image
        old_size = size_me(hd_path)
        ld_size = [old_size[0] / 5, old_size[1] / 5]

    # We build the command
    dst_path = hd_path.replace('.png', '_LD.png')
    cmd = '%s -y -i %s -vf scale=%i:%i %s' % (ffmpeg_dir, hd_path, ld_size[0], ld_size[1], dst_path)

    # We write Low def file
    print ffmpeg_dir, os.path.exists(ffmpeg_dir)
    os.system(cmd)


def size_me(path):
    """
    To get png image size

    # Official PNG binary structure (@ means byte) (http://www.w3.org/TR/PNG/#5PNG-file-signature)
    #
    #    signature     IHDR (image header)                other chunks...
    #    @@@@@@@@      @@@@ @@@@ @@@@ @@@@ @ @ @ @ @      @@@@@...
    #                   len code    w    h ....
    #
    # So, the first 8 + 4 + 4 = 16 bytes are useless for us.

    :param path: string: file path
    :return: list: [int, int]
    """

    png_handle = open(path, "rb")  # Open .png in binary format
    irrelevant_bytes = png_handle.read(16)  # Read the first useless 16 bytes
    print irrelevant_bytes
    ihdr_bytes = png_handle.read(8)  # IHDR bytes
    # The method struct.unpack(format, byteSequence) takes lowLevel data (bytes) and
    #  rebuild highLevel data (numbers, strings)
    # by following the chosen format; here it recovers two unsigned ints (the "!2I" format) from 4+4 bytes
    (width, height) = struct.unpack("!2I", ihdr_bytes)

    png_handle.close()

    return [width, height]


"""
# Example

vid_path = [r'Y:\01_SAISON_4\09_EPISODES\04_Fabrication_3D\YKR405\sh020\lay\preview\YKR405_020_lay_005.mov',
            r'Y:\01_SAISON_4\09_EPISODES\04_Fabrication_3D\YKR405\sh020\lay\preview\YKR405_020_lay_001.mov']

res_path = compare_videos_with_overlay(vid_path[0],vid_path[1])
"""
