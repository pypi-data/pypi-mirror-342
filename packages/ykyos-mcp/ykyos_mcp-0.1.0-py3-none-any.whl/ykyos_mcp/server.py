"""
MCP Server for URL Processing

This script implements a Model Context Protocol (MCP) server with three tools:
1. fetch_markdown: Takes a URL and returns its content as markdown by prepending https://r.jina.ai/
2. extract_images: Takes markdown content and extracts all image URLs
3. download_images: Takes a list of image URLs and downloads them to a specified directory
"""

import os
import re
import asyncio
import aiohttp
import aiofiles
from urllib.parse import urlparse, urljoin
from mcp.server.fastmcp import FastMCP, Context

# Get download path from environment variable
DOWNLOAD_BASE_PATH = os.environ.get('DOWNLOAD_BASE_PATH', './downloads')

# Initialize the MCP server
mcp = FastMCP("URL Processor and Image Extractor")

@mcp.tool()
async def fetch_markdown(url: str, ctx: Context = None) -> str:
    """
    Fetches content from a URL by prepending https://r.jina.ai/ to the URL.
    
    Args:
        url: The original URL to fetch content from
        ctx: MCP context for progress reporting
        
    Returns:
        str: The markdown content from the processed URL
    """
    # Create the processed URL by prepending https://r.jina.ai/
    processed_url = f"https://r.jina.ai/{url}"
    
    if ctx:
        ctx.info(f"Fetching content from {processed_url}")
    
    # Fetch the content from the processed URL
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(processed_url) as response:
                if response.status == 200:
                    content = await response.text()
                    if ctx:
                        ctx.info(f"Successfully fetched content ({len(content)} characters)")
                    return content
                else:
                    error_msg = f"Error: Failed to fetch content from {processed_url}. Status code: {response.status}"
                    if ctx:
                        ctx.error(error_msg)
                    return error_msg
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            if ctx:
                ctx.error(error_msg)
            return error_msg

@mcp.tool()
async def extract_images(markdown_content: str, ctx: Context = None) -> list:
    """
    Extracts all image URLs from markdown content.
    
    Args:
        markdown_content: Markdown content containing image references
        ctx: MCP context for progress reporting
        
    Returns:
        list: List of image URLs found in the markdown content
    """
    if ctx:
        ctx.info("Extracting image URLs from markdown content")
    
    # Regular expression patterns for Markdown image syntax
    # ![alt text](image_url) or <img src="image_url">
    markdown_pattern = r'!\[.*?\]\((.*?)\)'
    html_pattern = r'<img\s+[^>]*?src=[\'"]([^\'"]+)[\'"][^>]*?>'
    
    # Find all matches
    markdown_matches = re.findall(markdown_pattern, markdown_content)
    html_matches = re.findall(html_pattern, markdown_content)
    
    # Combine all matches
    all_images = markdown_matches + html_matches
    
    if ctx:
        ctx.info(f"Found {len(all_images)} image URLs in the content")
    
    # Return the list of image URLs
    return all_images

@mcp.tool()
async def download_images(image_urls: list, target_directory: str = None, ctx: Context = None) -> str:
    """
    Downloads images from a list of URLs to the specified directory.
    
    Args:
        image_urls: List of image URLs to download
        target_directory: Directory to save the downloaded images (defaults to DOWNLOAD_BASE_PATH)
        ctx: MCP context for progress reporting
        
    Returns:
        str: Status message with information about downloaded images
    """
    # If no target directory specified, use the environment variable
    if not target_directory:
        target_directory = DOWNLOAD_BASE_PATH
    
    if ctx:
        ctx.info(f"Preparing to download {len(image_urls)} images to {target_directory}")
    
    # Create the target directory if it doesn't exist
    os.makedirs(target_directory, exist_ok=True)
    
    successful_downloads = 0
    failed_downloads = 0
    download_details = []
    
    async with aiohttp.ClientSession() as session:
        download_tasks = []
        
        for url in image_urls:
            # Get the filename from the URL
            parsed_url = urlparse(url)
            filename = os.path.basename(parsed_url.path)
            
            # If filename is empty or doesn't have an extension, use a default name
            if not filename or '.' not in filename:
                filename = f"image_{len(download_tasks) + 1}.jpg"
            
            # Create full path for saving the image
            file_path = os.path.join(target_directory, filename)
            
            # Add download task
            download_task = asyncio.create_task(
                download_image(session, url, file_path, download_details, ctx)
            )
            download_tasks.append(download_task)
        
        # Wait for all downloads to complete
        for i, task in enumerate(asyncio.as_completed(download_tasks)):
            await task
            if ctx:
                # Report progress
                ctx.report_progress(i + 1, len(download_tasks))
    
    # Count successful and failed downloads
    for result in download_details:
        if result['success']:
            successful_downloads += 1
        else:
            failed_downloads += 1
    
    # Create status message
    status_message = f"Downloaded {successful_downloads} images to {target_directory}. "
    if failed_downloads > 0:
        status_message += f"Failed to download {failed_downloads} images."
    
    if ctx:
        ctx.info(status_message)
    
    return status_message

async def download_image(session, url, file_path, download_details, ctx=None):
    """Helper function to download an image."""
    try:
        if ctx:
            ctx.info(f"Downloading {url}")
        
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(await response.read())
                download_details.append({
                    'url': url,
                    'path': file_path,
                    'success': True
                })
                if ctx:
                    ctx.info(f"Successfully downloaded {url} to {file_path}")
            else:
                error_msg = f"HTTP Error: {response.status}"
                download_details.append({
                    'url': url,
                    'error': error_msg,
                    'success': False
                })
                if ctx:
                    ctx.error(f"Failed to download {url}: {error_msg}")
    except Exception as e:
        error_msg = str(e)
        download_details.append({
            'url': url,
            'error': error_msg,
            'success': False
        })
        if ctx:
            ctx.error(f"Error downloading {url}: {error_msg}")

# The main function is in __init__.py
# This allows the server to be run directly for testing
if __name__ == "__main__":
    # Run the MCP server
    print("Starting MCP server directly (for testing only)")
    mcp.run()