// Function to speak text
function speakText(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US'; // Set language (change dynamically based on translation language)
        window.speechSynthesis.speak(utterance);
    } else {
        alert('Your browser does not support text-to-speech.');
    }
}

// Add event listener to the speaker button
document.getElementById('speakerButton').addEventListener('click', function () {
    // Replace this with the actual translated text
    const translatedText = "This is the translated text."; // You can dynamically fetch this from your application logic
    speakText(translatedText); // Call the speakText function
});