import os
import tempfile
from typing import Dict, Any, Optional
import speech_recognition as sr
from pydub import AudioSegment
from pytube import YouTube
from moviepy import VideoFileClip

from datareader.processors.base_processor import BaseProcessor
from datareader.processors.audio_processor import AudioProcessor

class VideoProcessor(BaseProcessor):
    """
    Processor for extracting text from video files through transcription.
    """
    
    def process(self, source: str, **kwargs) -> str:
        """
        Process a video file or YouTube URL and extract its audio content as text.
        
        Args:
            source: Path to video file or YouTube URL.
            language: Language code for transcription (default: 'en-US').
            chunk_size: Size of audio chunks in milliseconds for processing (default: 60000).
            youtube_quality: YouTube video quality to download (default: "360p").
            **kwargs: Additional processing options.
            
        Returns:
            Transcribed text from the video.
        """
        is_youtube = source.startswith(('http://', 'https://')) and ('youtube.com' in source or 'youtu.be' in source)
        
        if is_youtube:
            # Download YouTube video
            temp_video_file = self._download_youtube_video(source, **kwargs)
            try:
                return self._process_video_file(temp_video_file, **kwargs)
            finally:
                # Clean up temporary file
                if os.path.exists(temp_video_file):
                    os.remove(temp_video_file)
        else:
            # Process local video file
            if not os.path.exists(source):
                raise FileNotFoundError(f"Video file not found: {source}")
            
            return self._process_video_file(source, **kwargs)
    
    def _download_youtube_video(self, url: str, **kwargs) -> str:
        """
        Download a YouTube video.
        
        Args:
            url: YouTube URL.
            youtube_quality: Video quality to download (default: "360p").
            
        Returns:
            Path to the downloaded video file.
        """
        quality = kwargs.get('youtube_quality', "360p")
        
        # Create a temporary file
        fd, temp_path = tempfile.mkstemp(suffix='.mp4')
        os.close(fd)
        
        # Download the video
        yt = YouTube(url)
        video = yt.streams.filter(progressive=True, file_extension='mp4', res=quality).first()
        
        # If requested quality not available, get the lowest quality
        if not video:
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').first()
        
        if not video:
            raise ValueError(f"No suitable video stream found for URL: {url}")
        
        video.download(filename=temp_path)
        return temp_path
    
    def _process_video_file(self, video_path: str, **kwargs) -> str:
        """
        Process a video file by extracting its audio and transcribing it.
        
        Args:
            video_path: Path to the video file.
            **kwargs: Additional processing options.
            
        Returns:
            Transcribed text from the video.
        """
        # Create temporary audio file
        fd, temp_audio_path = tempfile.mkstemp(suffix='.wav')
        os.close(fd)
        
        try:
            # Extract audio from video
            video = VideoFileClip(video_path)
            video.audio.write_audiofile(temp_audio_path, logger=None)
            
            # Use the audio processor to transcribe the audio
            audio_processor = AudioProcessor()
            return audio_processor.process(temp_audio_path, **kwargs)
        finally:
            # Clean up temporary audio file
            if os.path.exists(temp_audio_path):
                os.remove(temp_audio_path)
    
    def extract_metadata(self, source: str, **kwargs) -> Dict[str, Any]:
        """
        Extract metadata from a video file.
        
        Args:
            source: Path to the video file or YouTube URL.
            **kwargs: Additional options.
            
        Returns:
            Dictionary of video metadata.
        """
        metadata = {}
        
        is_youtube = source.startswith(('http://', 'https://')) and ('youtube.com' in source or 'youtu.be' in source)
        
        if is_youtube:
            # Extract YouTube metadata
            yt = YouTube(source)
            metadata = {
                'title': yt.title,
                'author': yt.author,
                'length_seconds': yt.length,
                'views': yt.views,
                'rating': yt.rating,
                'publish_date': str(yt.publish_date) if yt.publish_date else None,
                'description': yt.description,
                'url': source
            }
        else:
            # Extract local video metadata
            if not os.path.exists(source):
                raise FileNotFoundError(f"Video file not found: {source}")
            
            clip = VideoFileClip(source)
            metadata = {
                'duration': clip.duration,
                'fps': clip.fps,
                'size': clip.size,
                'filename': os.path.basename(source),
                'path': source
            }
            clip.close()
            
        return metadata 