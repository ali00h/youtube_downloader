const express = require('express');
const ytdl = require('ytdl-core');
const app = express();

app.get('/', async (req, res) => {
    const videoUrl = req.query.url;
    if (!videoUrl) {
        return res.status(400).send('Please provide a YouTube URL with ?url=');
    }

    try {
        // Validate the URL and get video info
        if (!ytdl.validateURL(videoUrl)) {
            return res.status(400).send('Invalid YouTube URL');
        }

        const info = await ytdl.getInfo(videoUrl);
        const format = ytdl.chooseFormat(info.formats, { quality: 'highestvideo' });

        // Set headers for video streaming
        res.setHeader('Content-Type', format.mimeType);
        res.setHeader('Content-Length', format.contentLength || '');

        // Stream the video to the client
        ytdl(videoUrl, { format: format }).pipe(res);
    } catch (error) {
        console.error(error);
        res.status(500).send('Error processing the video: ' + error.message);
    }
});

app.listen(3234, () => {
    console.log('Server running on port 3234');
});

