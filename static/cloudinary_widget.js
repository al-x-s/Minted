/**----------------------
 *    Cloudinary Upload Widget
 *------------------------**/

const audio_url_input = document.getElementById("audio_url")
const artwork_url_input = document.getElementById("artwork_url")

const audio_upload_widget = cloudinary.createUploadWidget({
  cloudName: 'dsd49h8kt', 
  uploadPreset: 'minted_music'}, (error, result) => { 
    if (!error && result && result.event === "success") {
      audio_url_input.value = result.info.url; 
    }
  }
)

const artwork_upload_widget = cloudinary.createUploadWidget({
  cloudName: 'dsd49h8kt', 
  uploadPreset: 'minted_artwork',
  cropping: true}, (error, result) => { 
    if (!error && result && result.event === "success") {
      artwork_url_input.value = result.info.url; 
    }
  }
)

