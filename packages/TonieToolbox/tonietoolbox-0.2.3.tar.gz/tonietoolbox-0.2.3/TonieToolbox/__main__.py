#!/usr/bin/python3
"""
Main entry point for the TonieToolbox package.
"""

import argparse
import os
import sys
import logging

from . import __version__
from .audio_conversion import get_input_files, append_to_filename
from .tonie_file import create_tonie_file
from .tonie_analysis import check_tonie_file, split_to_opus_files
from .dependency_manager import get_ffmpeg_binary, get_opus_binary
from .logger import setup_logging, get_logger
from .filename_generator import guess_output_filename
from .version_handler import check_for_updates, clear_version_cache
from .recursive_processor import process_recursive_folders
from .media_tags import is_available as is_media_tags_available, ensure_mutagen

def main():
    """Entry point for the TonieToolbox application."""
    parser = argparse.ArgumentParser(description='Create Tonie compatible file from Ogg opus file(s).')
    parser.add_argument('-v', '--version', action='version', version=f'TonieToolbox {__version__}',
                        help='show program version and exit')
    parser.add_argument('input_filename', metavar='SOURCE', type=str, 
                        help='input file or directory or a file list (.lst)')
    parser.add_argument('output_filename', metavar='TARGET', nargs='?', type=str,
                        help='the output file name (default: ---ID---)')
    parser.add_argument('-t', '--timestamp', dest='user_timestamp', metavar='TIMESTAMP', action='store',
                        help='set custom timestamp / bitstream serial')

    parser.add_argument('-f', '--ffmpeg', help='specify location of ffmpeg', default=None)
    parser.add_argument('-o', '--opusenc', help='specify location of opusenc', default=None)
    parser.add_argument('-b', '--bitrate', type=int, help='set encoding bitrate in kbps (default: 96)', default=96)
    parser.add_argument('-c', '--cbr', action='store_true', help='encode in cbr mode')
    parser.add_argument('-a', '--append-tonie-tag', metavar='TAG', action='store',
                        help='append [TAG] to filename (must be an 8-character hex value)')
    parser.add_argument('-n', '--no-tonie-header', action='store_true', help='do not write Tonie header')
    parser.add_argument('-i', '--info', action='store_true', help='Check and display info about Tonie file')
    parser.add_argument('-s', '--split', action='store_true', help='Split Tonie file into opus tracks')
    parser.add_argument('-r', '--recursive', action='store_true', help='Process folders recursively')
    parser.add_argument('-O', '--output-to-source', action='store_true', 
                        help='Save output files in the source directory instead of output directory')
    parser.add_argument('-A', '--auto-download', action='store_true', help='Automatically download FFmpeg and opusenc if needed')
    parser.add_argument('-k', '--keep-temp', action='store_true', 
                       help='Keep temporary opus files in a temp folder for testing')
    parser.add_argument('-u', '--use-legacy-tags', action='store_true',
                       help='Use legacy hardcoded tags instead of dynamic TonieToolbox tags')
    parser.add_argument('-C', '--compare', action='store', metavar='FILE2', 
                       help='Compare input file with another .taf file for debugging')
    parser.add_argument('-D', '--detailed-compare', action='store_true',
                       help='Show detailed OGG page differences when comparing files')
    
    # Media tag options
    media_tag_group = parser.add_argument_group('Media Tag Options')
    media_tag_group.add_argument('-m', '--use-media-tags', action='store_true',
                       help='Use media tags from audio files for naming')
    media_tag_group.add_argument('--name-template', metavar='TEMPLATE', action='store',
                       help='Template for naming files using media tags. Example: "{album} - {artist}"')
    media_tag_group.add_argument('--show-tags', action='store_true',
                       help='Show available media tags from input files')
    
    # Version check options
    version_group = parser.add_argument_group('Version Check Options')
    version_group.add_argument('-S', '--skip-update-check', action='store_true',
                       help='Skip checking for updates')
    version_group.add_argument('-F', '--force-refresh-cache', action='store_true',
                       help='Force refresh of update information from PyPI')
    version_group.add_argument('-X', '--clear-version-cache', action='store_true',
                       help='Clear cached version information')
    
    log_group = parser.add_argument_group('Logging Options')
    log_level_group = log_group.add_mutually_exclusive_group()
    log_level_group.add_argument('-d', '--debug', action='store_true', help='Enable debug logging')
    log_level_group.add_argument('-T', '--trace', action='store_true', help='Enable trace logging (very verbose)')
    log_level_group.add_argument('-q', '--quiet', action='store_true', help='Show only warnings and errors')
    log_level_group.add_argument('-Q', '--silent', action='store_true', help='Show only errors')

    args = parser.parse_args()
    if args.trace:
        from .logger import TRACE
        log_level = TRACE
    elif args.debug:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.WARNING
    elif args.silent:
        log_level = logging.ERROR
    else:
        log_level = logging.INFO

    setup_logging(log_level)
    logger = get_logger('main')
    logger.debug("Starting TonieToolbox v%s with log level: %s", __version__, logging.getLevelName(log_level))
    
    if args.clear_version_cache:
        if clear_version_cache():
            logger.info("Version cache cleared successfully")
        else:
            logger.info("No version cache to clear or error clearing cache")
    
    if not args.skip_update_check:
        logger.debug("Checking for updates (force_refresh=%s)", args.force_refresh_cache)
        is_latest, latest_version, message, update_confirmed = check_for_updates(
            quiet=args.silent or args.quiet,
            force_refresh=args.force_refresh_cache
        )
        
        if not is_latest and not update_confirmed and not (args.silent or args.quiet):
            logger.info("Update available but user chose to continue without updating.")

    ffmpeg_binary = args.ffmpeg
    if ffmpeg_binary is None:
        ffmpeg_binary = get_ffmpeg_binary(args.auto_download)
        if ffmpeg_binary is None:
            logger.error("Could not find FFmpeg. Please install FFmpeg or specify its location using --ffmpeg or use --auto-download")
            sys.exit(1)
        logger.debug("Using FFmpeg binary: %s", ffmpeg_binary)

    opus_binary = args.opusenc
    if opus_binary is None:
        opus_binary = get_opus_binary(args.auto_download) 
        if opus_binary is None:
            logger.error("Could not find opusenc. Please install opus-tools or specify its location using --opusenc or use --auto-download")
            sys.exit(1)
        logger.debug("Using opusenc binary: %s", opus_binary)

    # Check for media tags library and handle --show-tags option
    if (args.use_media_tags or args.show_tags or args.name_template) and not is_media_tags_available():
        if not ensure_mutagen(auto_install=args.auto_download):
            logger.warning("Media tags functionality requires the mutagen library but it could not be installed.")
            if args.use_media_tags or args.show_tags:
                logger.error("Cannot proceed with --use-media-tags or --show-tags without mutagen library")
                sys.exit(1)
        else:
            logger.info("Successfully enabled media tag support")

    # Handle recursive processing
    if args.recursive:
        logger.info("Processing folders recursively: %s", args.input_filename)
        process_tasks = process_recursive_folders(
            args.input_filename,
            use_media_tags=args.use_media_tags,
            name_template=args.name_template
        )
        
        if not process_tasks:
            logger.error("No folders with audio files found for recursive processing")
            sys.exit(1)
            
        output_dir = None if args.output_to_source else './output'
        
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
            logger.debug("Created output directory: %s", output_dir)
        
        for task_index, (output_name, folder_path, audio_files) in enumerate(process_tasks):
            if args.output_to_source:
                task_out_filename = os.path.join(folder_path, f"{output_name}.taf")
            else:
                task_out_filename = os.path.join(output_dir, f"{output_name}.taf")
                
            logger.info("[%d/%d] Processing folder: %s -> %s", 
                      task_index + 1, len(process_tasks), folder_path, task_out_filename)
            
            create_tonie_file(task_out_filename, audio_files, args.no_tonie_header, args.user_timestamp,
                           args.bitrate, not args.cbr, ffmpeg_binary, opus_binary, args.keep_temp, 
                           args.auto_download, not args.use_legacy_tags)
            logger.info("Successfully created Tonie file: %s", task_out_filename)
            
        logger.info("Recursive processing completed. Created %d Tonie files.", len(process_tasks))
        sys.exit(0)

    # Handle directory or file input
    if os.path.isdir(args.input_filename):
        logger.debug("Input is a directory: %s", args.input_filename)
        args.input_filename += "/*"
    else:
        logger.debug("Input is a file: %s", args.input_filename)
        if args.info:
            logger.info("Checking Tonie file: %s", args.input_filename)
            ok = check_tonie_file(args.input_filename)
            sys.exit(0 if ok else 1)
        elif args.split:
            logger.info("Splitting Tonie file: %s", args.input_filename)
            split_to_opus_files(args.input_filename, args.output_filename)
            sys.exit(0)
        elif args.compare:
            from .tonie_analysis import compare_taf_files
            logger.info("Comparing Tonie files: %s and %s", args.input_filename, args.compare)
            result = compare_taf_files(args.input_filename, args.compare, args.detailed_compare)
            sys.exit(0 if result else 1)

    files = get_input_files(args.input_filename)
    logger.debug("Found %d files to process", len(files))

    if len(files) == 0:
        logger.error("No files found for pattern %s", args.input_filename)
        sys.exit(1)

    # Show tags for input files if requested
    if args.show_tags:
        from .media_tags import get_file_tags
        logger.info("Showing media tags for input files:")
        
        for file_index, file_path in enumerate(files):
            tags = get_file_tags(file_path)
            if tags:
                print(f"\nFile {file_index + 1}: {os.path.basename(file_path)}")
                print("-" * 40)
                for tag_name, tag_value in sorted(tags.items()):
                    print(f"{tag_name}: {tag_value}")
            else:
                print(f"\nFile {file_index + 1}: {os.path.basename(file_path)} - No tags found")
        
        sys.exit(0)
        
    # Use media tags for file naming if requested
    guessed_name = None
    if args.use_media_tags:
        # If this is a single folder, try to get consistent album info
        if len(files) > 1 and os.path.dirname(files[0]) == os.path.dirname(files[-1]):
            folder_path = os.path.dirname(files[0])
            
            from .media_tags import extract_album_info, format_metadata_filename
            logger.debug("Extracting album info from folder: %s", folder_path)
            
            album_info = extract_album_info(folder_path)
            if album_info:
                # Use album info for naming the output file
                template = args.name_template or "{album} - {artist}"
                new_name = format_metadata_filename(album_info, template)
                
                if new_name:
                    logger.info("Using album metadata for output filename: %s", new_name)
                    guessed_name = new_name
                else:
                    logger.debug("Could not format filename from album metadata")
        
        # For single files, use the file's metadata
        elif len(files) == 1:
            from .media_tags import get_file_tags, format_metadata_filename
            
            tags = get_file_tags(files[0])
            if tags:
                template = args.name_template or "{title} - {artist}"
                new_name = format_metadata_filename(tags, template)
                
                if new_name:
                    logger.info("Using file metadata for output filename: %s", new_name)
                    guessed_name = new_name
                else:
                    logger.debug("Could not format filename from file metadata")
        
        # For multiple files from different folders, try to use common tags if they exist
        elif len(files) > 1:
            from .media_tags import get_file_tags, format_metadata_filename
            
            # Try to find common tags among files
            common_tags = {}
            for file_path in files:
                tags = get_file_tags(file_path)
                if tags:
                    for key, value in tags.items():
                        if key in ['album', 'albumartist', 'artist']:
                            if key not in common_tags:
                                common_tags[key] = value
                            # Only keep values that are the same across files
                            elif common_tags[key] != value:
                                common_tags[key] = None
            
            # Remove None values
            common_tags = {k: v for k, v in common_tags.items() if v is not None}
            
            if common_tags:
                template = args.name_template or "Collection - {album}" if 'album' in common_tags else "Collection"
                new_name = format_metadata_filename(common_tags, template)
                
                if new_name:
                    logger.info("Using common metadata for output filename: %s", new_name)
                    guessed_name = new_name
                else:
                    logger.debug("Could not format filename from common metadata")

    if args.output_filename:
        out_filename = args.output_filename
    elif guessed_name:
        if args.output_to_source:
            source_dir = os.path.dirname(files[0]) if files else '.'
            out_filename = os.path.join(source_dir, guessed_name)
            logger.debug("Using source location for output with media tags: %s", out_filename)
        else:
            output_dir = './output'
            if not os.path.exists(output_dir):
                logger.debug("Creating default output directory: %s", output_dir)
                os.makedirs(output_dir, exist_ok=True)
            out_filename = os.path.join(output_dir, guessed_name)
            logger.debug("Using default output location with media tags: %s", out_filename)
    else:
        guessed_name = guess_output_filename(args.input_filename, files)    
        if args.output_to_source:
            source_dir = os.path.dirname(files[0]) if files else '.'
            out_filename = os.path.join(source_dir, guessed_name)
            logger.debug("Using source location for output: %s", out_filename)
        else:
            output_dir = './output'
            if not os.path.exists(output_dir):
                logger.debug("Creating default output directory: %s", output_dir)
                os.makedirs(output_dir, exist_ok=True)
            out_filename = os.path.join(output_dir, guessed_name)
            logger.debug("Using default output location: %s", out_filename)

    if args.append_tonie_tag:
        logger.debug("Appending Tonie tag to output filename")
        hex_tag = args.append_tonie_tag
        logger.debug("Validating tag: %s", hex_tag)
        if not all(c in '0123456789abcdefABCDEF' for c in hex_tag) or len(hex_tag) != 8:
            logger.error("TAG must be an 8-character hexadecimal value")
            sys.exit(1)
        logger.debug("Appending [%s] to output filename", hex_tag)
        out_filename = append_to_filename(out_filename, hex_tag)
    
    if not out_filename.lower().endswith('.taf'):
        out_filename += '.taf'
    
    logger.info("Creating Tonie file: %s with %d input file(s)", out_filename, len(files))
    create_tonie_file(out_filename, files, args.no_tonie_header, args.user_timestamp,
                     args.bitrate, not args.cbr, ffmpeg_binary, opus_binary, args.keep_temp, 
                     args.auto_download, not args.use_legacy_tags)
    logger.info("Successfully created Tonie file: %s", out_filename)


if __name__ == "__main__":
    main()