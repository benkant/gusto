# Automating Apple Music Recordings with Audio Hijack

Audio Hijack is a powerful tool for recording audio from various sources on macOS, including Apple Music. While you can manually record songs, automating the process for an entire playlist or collection of songs requires a scripting approach. This comprehensive guide will walk you through setting up an automated system to record Apple Music songs as individual WAV files using Audio Hijack's scripting capabilities.

## Understanding Audio Hijack's Scripting Capabilities

Audio Hijack provides robust scripting support through both its JavaScript API and AppleScript integration. The application allows you to create scripts that can control recording sessions, process files after recording, and interact with other applications[5][16][17].

### Key Scripting Features

- **JavaScript API**: Audio Hijack runs scripts using macOS's built-in JavaScript engine (the same used by Safari)[16]
- **Global Objects**: Scripts have access to `app` and `console` objects for controlling Audio Hijack[16]
- **Event-Based Triggers**: Scripts can respond to events like recording start/stop[5][16]
- **Shell Command Integration**: You can execute shell commands from within scripts[16]
- **Shortcuts Integration**: Scripts can trigger Apple Shortcuts for additional functionality[5][16]

## Solution Overview

The approach to automate recording Apple Music tracks will involve:

1. Setting up an Audio Hijack session specifically configured for Apple Music
2. Creating a script that can process a list of song URLs
3. Automating the playback and recording cycle for each song
4. Organizing and naming the resulting WAV files

## Step 1: Basic Audio Hijack Session Setup

First, you'll need to configure a dedicated session in Audio Hijack:

1. Open Audio Hijack and create a new session
2. Add an "Application" source block and select Apple Music
3. Connect this to a "Recorder" block
4. In the Recorder block settings:
   - Set the format to WAV
   - Configure your desired bit depth and sample rate
   - Choose an output folder for your recordings

## Step 2: Create a Script for Processing Apple Music URLs

You'll need a script that can:
- Read URLs from a text file or process a playlist URL
- Control Apple Music to play each song
- Manage the recording process in Audio Hijack

Here's a script combining JavaScript (for Audio Hijack) and AppleScript (for controlling Apple Music):

```javascript
// #needsFile
// Script to automate recording of Apple Music songs from a URL list

// Configuration
const SONGS_FILE = "/path/to/your/songs.txt"; // Path to text file with Apple Music URLs
const OUTPUT_FOLDER = "/path/to/your/recordings/"; // Where to save WAV files
const BUFFER_TIME = 3; // Extra seconds to record after song ends (for safety)
const SESSION_NAME = "Apple Music Recording"; // Your Audio Hijack session name

// Get the Audio Hijack session
function getSession() {
    const session = app.sessionWithName(SESSION_NAME);
    if (!session) {
        console.error("Session not found: " + SESSION_NAME);
        return null;
    }
    return session;
}

// Read song URLs from file
function readSongUrls() {
    const [status, stdout, stderr] = app.runShellCommand(`cat "${SONGS_FILE}"`);
    if (status !== 0) {
        console.error("Failed to read songs file: " + stderr);
        return [];
    }
    return stdout.split("\n").filter(url => url.trim() !== "");
}

// Main process function
function processSongs() {
    const session = getSession();
    if (!session) return;
    
    const songUrls = readSongUrls();
    console.log(`Found ${songUrls.length} songs to process`);
    
    // Process each song
    for (let i = 0; i < songUrls.length; i++) {
        const url = songUrls[i];
        console.log(`Processing song ${i+1}/${songUrls.length}: ${url}`);
        
        // Start playing the song in Apple Music
        const script = `
            tell application "Music"
                open location "${url}"
                delay 1
                set currentTrack to current track
                set trackName to name of currentTrack
                set artistName to artist of currentTrack
                set songDuration to duration of currentTrack
                play
                return {trackName, artistName, songDuration}
            end tell
        `;
        
        const [scriptStatus, scriptOutput, scriptError] = app.runShellCommand(`osascript -e '${script}'`);
        if (scriptStatus !== 0) {
            console.error("Failed to play song: " + scriptError);
            continue;
        }
        
        // Parse track info from AppleScript result
        const trackInfo = scriptOutput.split(", ");
        const trackName = trackInfo[0].replace(/^"|"$/g, "");
        const artistName = trackInfo[1].replace(/^"|"$/g, "");
        const songDuration = parseFloat(trackInfo[2]);
        
        // Configure the session for this song
        session.recordings[0].filePath = `${OUTPUT_FOLDER}${artistName} - ${trackName}.wav`;
        
        // Start recording
        if (!session.running) {
            session.start();
        } else {
            session.recording.start();
        }
        
        console.log(`Recording "${trackName}" by ${artistName} (${songDuration} seconds)`);
        
        // Wait for song to complete plus buffer time
        app.runShellCommand(`sleep ${songDuration + BUFFER_TIME}`);
        
        // Stop recording
        session.recording.stop();
        
        // Wait for file processing
        app.runShellCommand("sleep 2");
    }
    
    // Stop the session
    if (session.running) {
        session.stop();
    }
    
    console.log("All songs processed!");
}

// Run the main process
processSongs();
```

## Step 3: Handling Playlist URLs

If you want to process an entire Apple Music playlist instead of individual song URLs, you'll need to extract the songs from the playlist first. This requires a slightly different approach:

```javascript
// Function to extract songs from a playlist URL
function processMusicPlaylist(playlistUrl) {
    const script = `
        tell application "Music"
            open location "${playlistUrl}"
            delay 3
            set songList to {}
            set trackCount to count of tracks in current playlist
            repeat with i from 1 to trackCount
                set trackData to {name of track i of current playlist, artist of track i of current playlist, duration of track i of current playlist}
                copy trackData to the end of songList
            end repeat
            return songList
        end tell
    `;
    
    const [status, output, error] = app.runShellCommand(`osascript -e '${script}'`);
    if (status !== 0) {
        console.error("Failed to process playlist: " + error);
        return [];
    }
    
    // Parse the output to get song information
    const lines = output.split("\n");
    const songs = [];
    for (let i = 0; i < lines.length; i += 3) {
        if (i + 2 < lines.length) {
            songs.push({
                name: lines[i].trim(),
                artist: lines[i+1].trim(),
                duration: parseFloat(lines[i+2])
            });
        }
    }
    
    return songs;
}
```

## Step 4: Setting Up Automatic Track Marking

Audio Hijack can automatically split recordings at natural track boundaries, which is useful if you're recording a continuous playlist[12]. To enable this:

1. In your Recording block, check "Add tracks automatically"
2. Configure silence detection settings (typically 2 seconds of silence works well)
3. Enable "Split at track markers" to create separate files for each track

## Advanced Customization Options

### Metadata Tagging

You can automatically tag your recordings with metadata like artist, album, and track number[14][19]:

```javascript
// Add metadata to the recording
function applyMetadata(filePath, title, artist, album, trackNumber) {
    const escapedPath = app.shellEscapeArgument(filePath);
    const escapedTitle = app.shellEscapeArgument(title);
    const escapedArtist = app.shellEscapeArgument(artist);
    const escapedAlbum = app.shellEscapeArgument(album);
    
    const command = `afinfo -m ${escapedPath} ` +
                    `--title ${escapedTitle} ` +
                    `--artist ${escapedArtist} ` +
                    `--album ${escapedAlbum} ` +
                    `--track ${trackNumber}`;
    
    app.runShellCommand(command);
}
```

### Post-Processing with Scripts

Audio Hijack allows you to run scripts after recording completes[5][11][16]. This can be used to automatically:

1. Add recordings to Apple Music (previously iTunes)[8][17]
2. Process the audio (e.g., normalize volume, trim silence)
3. Move files to specific folders based on metadata

## Important Considerations

### Legal and Ethical Concerns

Recording from Apple Music should be for personal use only. The service's terms of use generally prohibit copying or distributing their content. This solution should only be used for:

- Creating personal backups of music you have rights to
- Time-shifting content for personal consumption
- Educational or fair use purposes

### Technical Limitations

1. **DRM Protection**: Apple Music includes DRM protection that may interfere with recording quality[9]
2. **System Audio Changes**: macOS updates may change how audio is routed, requiring script adjustments[10]
3. **Recording Quality**: The audio quality will depend on your playback settings in Apple Music[13]

### Alternative Approaches

If you encounter difficulties with this script-based approach, consider these alternatives:

1. **Use Blackhole**: A virtual audio driver that can route audio between applications[13]
2. **Audio Hijack with Loopback**: Combines these two Rogue Amoeba products for more complex audio routing[4]
3. **Purchase from iTunes Store**: If available, purchasing from iTunes Store provides DRM-free files that don't require recording[2]

## Conclusion

Audio Hijack offers powerful scripting capabilities that can automate the recording process for Apple Music tracks. By combining JavaScript for Audio Hijack control with AppleScript for Apple Music control, you can create a system that processes a list of songs or an entire playlist and saves each as an individual WAV file.

For the most reliable results, you may need to adjust timeout values and silence detection settings based on your network speed and the specific characteristics of the music you're recording. The scripting approach offers flexibility to customize the process to your exact needs.

The solution outlined here provides a starting point that you can modify and extend based on your specific requirements and technical comfort level.

Sources
[1] ?showArticle=AH-Scripting-API%3F https://rogueamoeba.com/support/knowledgebase/?showArticle=AH-Scripting-API%3F
[2] Is there an easy way to move music from Apple Music and ... https://www.reddit.com/r/finalcutpro/comments/12ldsdm/is_there_an_easy_way_to_move_music_from_apple/
[3] Audio Hijack, the (Mac) DJ's Secret Recording Weapon https://www.reddit.com/r/DJs/comments/1631fsn/audio_hijack_the_mac_djs_secret_recording_weapon/
[4] Theoretically, could someone stream audio from their ... https://www.reddit.com/r/protools/comments/gth4y9/theoretically_could_someone_stream_audio_from/
[5] Audio Hijack Manual — Scripting and Automation - Rogue Amoeba https://rogueamoeba.com/support/manuals/audiohijack/?page=scripting
[6] SoundSource vs Audio Hijack : r/macapps https://www.reddit.com/r/macapps/comments/1fekybw/soundsource_vs_audio_hijack/
[7] Recording Computer Audio into Handheld Recorder for ... https://www.reddit.com/r/musicproduction/comments/vgghs5/recording_computer_audio_into_handheld_recorder/
[8] Integrating Audio Hijack Pro and iTunes - Davinder Mahal https://www.mahal.org/articles/integrating-audio-hijack-pro-and-itunes/
[9] Apple Music to AUM : r/ipadmusic https://www.reddit.com/r/ipadmusic/comments/qodjed/apple_music_to_aum/
[10] It's time for MacOS to be able to natively record computer ... https://www.reddit.com/r/MacOS/comments/1cjbeb6/its_time_for_macos_to_be_able_to_natively_record/
[11] Creating a script from start to finish - Rogue Amoeba https://rogueamoeba.com/support/knowledgebase/?showArticle=AH-Scripting-CreationExample
[12] How to split music files into individual songs : r/macapps https://www.reddit.com/r/macapps/comments/1e3of7r/how_to_split_music_files_into_individual_songs/
[13] Setting up EQ for MacOS : r/oratory1990 https://www.reddit.com/r/oratory1990/comments/qi8s6h/setting_up_eq_for_macos/
[14] Use Audio Hijack Pro to record Spotify tracks while you listen · GitHub https://gist.github.com/iolloyd/3604106
[15] Recording from Apple Music lossless to optical out ... https://www.reddit.com/r/minidisc/comments/18d680f/recording_from_apple_music_lossless_to_optical/
[16] A complete scripting API reference for Audio Hijack - Rogue Amoeba https://rogueamoeba.com/support/knowledgebase/?showArticle=AH-Scripting-API
[17] Audio Hijack Pro to iTunes script - All this - Dr. Drang https://leancrew.com/all-this/2008/09/audio-hijack-pro-to-itunes-script/
[18] Audio Hijack Manual — Sidebar Controls - Rogue Amoeba https://rogueamoeba.com/support/manuals/audiohijack/?page=sidebarcontrols
[19] Spot the Hijack - GitHub Gist https://gist.github.com/tiffanygwilson/1914c3b7724e65d736f6
[20] Help- Panicking and running out of ideas! : r/qlab https://www.reddit.com/r/qlab/comments/1jjwpjr/help_panicking_and_running_out_of_ideas/
[21] Apple releases LOGIC PRO X - Featuring iPad control, Flex ... https://www.reddit.com/r/WeAreTheMusicMakers/comments/1ietre/apple_releases_logic_pro_x_featuring_ipad_control/
[22] OSX software favorites.. What is your personal "must have" ... https://www.reddit.com/r/osx/comments/2lo447/osx_software_favorites_what_is_your_personal_must/
[23] iOS 18: AI tools for summarizing audio recordings coming https://www.reddit.com/r/apple/comments/1d3ni34/ios_18_ai_tools_for_summarizing_audio_recordings/
[24] Mac program that does timed recordings? : r/MacOS https://www.reddit.com/r/MacOS/comments/u59b3e/mac_program_that_does_timed_recordings/
[25] Audio Routing Kit (ARK) Icon From Sound Source App ... https://www.reddit.com/r/macapps/comments/1g0dzn4/audio_routing_kit_ark_icon_from_sound_source_app/
[26] What are your favorite tools for podcasting? https://www.reddit.com/r/podcasting/comments/ok62ya/what_are_your_favorite_tools_for_podcasting/
[27] Pros & cons - eqMac vs SoundSource vs Toneboosters EQ ... https://www.reddit.com/r/oratory1990/comments/197z2jj/pros_cons_eqmac_vs_soundsource_vs_toneboosters_eq/
[28] Recording System Audio On MacOS : r/electronjs https://www.reddit.com/r/electronjs/comments/1d9bjh9/recording_system_audio_on_macos/
[29] Switching to Apple Music from Spotify : r/sonos https://www.reddit.com/r/sonos/comments/11wlqww/switching_to_apple_music_from_spotify/
[30] MacOS tools to make your life easier https://www.reddit.com/r/MacOS/comments/18d6ljq/macos_tools_to_make_your_life_easier/
[31] Doug's AppleScripts June 2017 https://dougscripts.com/itunes/2017/06/
[32] Audio Hijack 4, Shortcuts, Podcasting Automation - Robby Burns http://www.robbyburns.com/blog/audio-hijack
[33] Splitting recording in Audio Hijack Pro on spotify track change ... https://stackoverflow.com/questions/8567783/splitting-recording-in-audio-hijack-pro-on-spotify-track-change-applescript
[34] Example scripts for Audio Hijack - Rogue Amoeba https://rogueamoeba.com/support/knowledgebase/?showArticle=AH-Scripting-SampleScripts
[35] r/ios on Reddit: Is there a way to play music from your playlists in the ... https://www.reddit.com/r/ios/comments/1av0nnl/is_there_a_way_to_play_music_from_your_playlists/
[36] Automating Audio Hijack 4 with Shortcuts and JavaScript - Six Colors https://sixcolors.com/post/2022/03/automating-audio-hijack-4-with-shortcuts-and-javascript/
[37] Audio Hijack 3 and scripts - Primary Unit https://www.robjwells.com/2015/01/audio-hijack-3-and-scripts/
[38] Audio Hijack & Loopback Tutorial for Advanced Mac Recordings https://www.youtube.com/watch?v=cOA2Ex3AsCM
[39] Audio Hijack Manual - Rogue Amoeba https://rogueamoeba.com/support/manuals/audiohijack/?print=true
[40] How to Record Multiple Tracks with Audio Hijack - YouTube https://www.youtube.com/watch?v=ADuaMIVd7nE
[41] Is there any way to roll in audio played on mac to logic? - Reddit https://www.reddit.com/r/Logic_Studio/comments/1chhqkg/is_there_any_way_to_roll_in_audio_played_on_mac/
[42] Has AUAudioFilePlayer been disabled in Logic Pro 10.8? https://www.reddit.com/r/Logic_Studio/comments/18a4z4w/has_auaudiofileplayer_been_disabled_in_logic_pro/
[43] Airplay recorder alternative for Music App : r/osx https://www.reddit.com/r/osx/comments/f1xip8/airplay_recorder_alternative_for_music_app/
[44] Is there a "TuneUp" alternative for the Apple Music app? https://www.reddit.com/r/AppleMusic/comments/gfdopg/is_there_a_tuneup_alternative_for_the_apple_music/
[45] Recording Streaming Audio to use in Logic X? https://www.reddit.com/r/Logic_Studio/comments/9alalt/recording_streaming_audio_to_use_in_logic_x/
[46] Apple rebuilding Apple Music in macOS Monterey 12.2 as ... https://www.reddit.com/r/MacOS/comments/ri365s/apple_rebuilding_apple_music_in_macos_monterey/
[47] SoundSource vs Audio Hijack : r/macapps https://www.reddit.com/r/macapps/comments/1fekybw/soundsource_vs_audio_hijack/
[48] AudioRecorder.app - Effortless Audio Recording on macOS https://www.reddit.com/r/macapps/comments/1j8z5r1/audiorecorderapp_effortless_audio_recording_on/
[49] Collaborative Playlist Hijacked : r/spotify https://www.reddit.com/r/spotify/comments/jt299m/collaborative_playlist_hijacked/
[50] Mac friendly way to record audio via Skype/Zoom ... https://www.reddit.com/r/podcasts/comments/bpk5c2/mac_friendly_way_to_record_audio_via_skypezoom/
[51] Metadata Not Appearing in Audio Hijack - Apple Support Communities https://discussions.apple.com/thread/252201472
[52] Audio Hijack, the (Mac) DJ's Secret Recording Weapon : r/DJs - Reddit https://www.reddit.com/r/DJs/comments/1631fsn/audio_hijack_the_mac_djs_secret_recording_weapon/
[53] Music Editing with Audio Hijack or WireTap - Apple Community https://discussions.apple.com/thread/2166590
[54] Mac mainstay Audio Hijack adds automation transcription https://appleinsider.com/articles/23/11/03/mac-mainstay-audio-hijack-adds-automation-transcription
[55] Audio Hijack Supports Scripting Again! (Help Running Scripts From ... https://forum.keyboardmaestro.com/t/audio-hijack-supports-scripting-again-help-running-scripts-from-km/27170
[56] Sample from Apple Music on iOS? : r/ipadmusic https://www.reddit.com/r/ipadmusic/comments/axujns/sample_from_apple_music_on_ios/
[57] Is there a way to record the audio I'm getting with ... https://www.reddit.com/r/protools/comments/kgzkri/is_there_a_way_to_record_the_audio_im_getting/
[58] [P] I trained an AI model on 120M+ songs from iTunes https://www.reddit.com/r/MachineLearning/comments/10st28f/p_i_trained_an_ai_model_on_120m_songs_from_itunes/
[59] How to automate audio recordings and uploads to the cloud? https://www.reddit.com/r/mac/comments/161yqgl/how_to_automate_audio_recordings_and_uploads_to/
[60] Audio Hijack: Record Any Audio on MacOS - Rogue Amoeba https://rogueamoeba.com/audiohijack/
[61] How to record any audio from the web with Audio Hijack 3 on the Mac https://www.imore.com/how-record-any-audio-web-audio-hijack-3-mac
[62] How to capture audio from iOS devices in Audio Hijack https://rogueamoeba.com/support/knowledgebase/?showArticle=Misc-iOSRecording&product=Audio+Hijack
[63] Audio Hijack Pro to iTunes script - All this - Dr. Drang https://leancrew.com/all-this/2008/09/audio-hijack-pro-to-itunes-script/
[64] How to Keep Recordings the Same Length with Audio Hijack https://www.youtube.com/watch?v=24Je33MEyfw
