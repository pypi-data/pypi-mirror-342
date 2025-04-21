"""
Media handling utilities for Gpgram.

This module provides utilities for working with media files in Telegram bots.
"""

import os
import io
import aiohttp
import asyncio
from typing import Union, Optional, BinaryIO, List, Dict, Any, Tuple
from pathlib import Path

from ..logging import get_logger

logger = get_logger(__name__)


async def download_file(file_id: str, bot, destination: Optional[Union[str, Path, BinaryIO]] = None) -> Union[bytes, str, None]:
    """
    Download a file from Telegram.
    
    Args:
        file_id: File ID to download
        bot: Bot instance
        destination: Destination to save the file to. Can be a file path, a Path object, or a file-like object.
                    If None, the file content is returned as bytes.
    
    Returns:
        If destination is None, returns the file content as bytes.
        If destination is a file path or Path object, returns the path as a string.
        If destination is a file-like object, returns None.
    """
    try:
        # Get file info
        file_info = await bot.get_file(file_id=file_id)
        if not file_info or 'file_path' not in file_info:
            logger.error(f"Failed to get file info for file_id: {file_id}")
            return None
        
        file_path = file_info['file_path']
        file_url = f"https://api.telegram.org/file/bot{bot.token}/{file_path}"
        
        # Download the file
        async with aiohttp.ClientSession() as session:
            async with session.get(file_url) as response:
                if response.status != 200:
                    logger.error(f"Failed to download file: {response.status}")
                    return None
                
                content = await response.read()
                
                # Return content as bytes if no destination is provided
                if destination is None:
                    return content
                
                # Save to file path
                if isinstance(destination, (str, Path)):
                    path = Path(destination)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    with open(path, 'wb') as f:
                        f.write(content)
                    return str(path)
                
                # Write to file-like object
                if hasattr(destination, 'write'):
                    destination.write(content)
                    return None
                
                logger.error(f"Invalid destination type: {type(destination)}")
                return None
    except Exception as e:
        logger.exception(f"Error downloading file: {e}")
        return None


async def upload_media_group(
    chat_id: int,
    media: List[Dict[str, Any]],
    bot,
    disable_notification: Optional[bool] = None,
    reply_to_message_id: Optional[int] = None,
    allow_sending_without_reply: Optional[bool] = None,
) -> List[Dict[str, Any]]:
    """
    Send a group of photos, videos, documents or audios as an album.
    
    Args:
        chat_id: Unique identifier for the target chat
        media: A list of InputMedia objects describing the media to send
        bot: Bot instance
        disable_notification: Sends the message silently
        reply_to_message_id: If the message is a reply, ID of the original message
        allow_sending_without_reply: Pass True if the message should be sent even if the specified replied-to message is not found
    
    Returns:
        List of sent messages
    """
    try:
        return await bot.send_media_group(
            chat_id=chat_id,
            media=media,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            allow_sending_without_reply=allow_sending_without_reply,
        )
    except Exception as e:
        logger.exception(f"Error sending media group: {e}")
        return []


async def create_media_group(
    media_type: str,
    media_files: List[Union[str, BinaryIO, Tuple[Union[str, BinaryIO], str]]],
    caption: Optional[str] = None,
    parse_mode: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Create a media group for sending multiple media files.
    
    Args:
        media_type: Type of media ('photo', 'video', 'document', 'audio')
        media_files: List of media files. Each item can be:
                    - A file path or URL
                    - A file-like object
                    - A tuple of (file, caption) where caption is specific to that media item
        caption: Caption for the entire media group (used if individual captions are not provided)
        parse_mode: Parse mode for the caption
    
    Returns:
        List of InputMedia objects ready to be sent with send_media_group
    """
    if media_type not in ('photo', 'video', 'document', 'audio'):
        raise ValueError(f"Invalid media type: {media_type}")
    
    media_group = []
    
    for i, media_item in enumerate(media_files):
        item_caption = None
        media_file = media_item
        
        # Handle tuple of (file, caption)
        if isinstance(media_item, tuple) and len(media_item) == 2:
            media_file, item_caption = media_item
        
        # Use group caption for the first item if no individual caption is provided
        if i == 0 and item_caption is None and caption:
            item_caption = caption
        
        media_dict = {
            'type': media_type,
            'media': media_file,
        }
        
        if item_caption:
            media_dict['caption'] = item_caption
            if parse_mode:
                media_dict['parse_mode'] = parse_mode
        
        media_group.append(media_dict)
    
    return media_group


async def download_profile_photos(user_id: int, bot, destination_folder: Union[str, Path], limit: int = 1) -> List[str]:
    """
    Download profile photos for a user.
    
    Args:
        user_id: User ID
        bot: Bot instance
        destination_folder: Folder to save photos to
        limit: Maximum number of photos to download
    
    Returns:
        List of paths to downloaded photos
    """
    try:
        # Get user profile photos
        photos = await bot.get_user_profile_photos(user_id=user_id, limit=limit)
        if not photos or 'photos' not in photos or not photos['photos']:
            logger.info(f"No profile photos found for user {user_id}")
            return []
        
        # Create destination folder
        folder = Path(destination_folder)
        folder.mkdir(parents=True, exist_ok=True)
        
        downloaded_paths = []
        
        # Download each photo (use the largest size)
        for i, photo_sizes in enumerate(photos['photos']):
            if not photo_sizes:
                continue
            
            # Get the largest photo (last in the list)
            photo = photo_sizes[-1]
            file_id = photo.get('file_id')
            
            if not file_id:
                continue
            
            # Download the photo
            file_path = os.path.join(folder, f"user_{user_id}_photo_{i}.jpg")
            result = await download_file(file_id, bot, file_path)
            
            if result:
                downloaded_paths.append(result)
        
        return downloaded_paths
    except Exception as e:
        logger.exception(f"Error downloading profile photos: {e}")
        return []
