/**
 * Happy Scroll AI - Background Service Worker
 * 
 * This service worker handles extension lifecycle events and can be extended
 * for additional functionality like caching, notifications, etc.
 */

// Extension installation/update handler
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('[Happy Scroll AI] Extension installed successfully!');
    console.log('[Happy Scroll AI] Visit YouTube Shorts to start automatic safety filtering.');
  } else if (details.reason === 'update') {
    console.log('[Happy Scroll AI] Extension updated to version', chrome.runtime.getManifest().version);
  }
});

// Extension startup handler
chrome.runtime.onStartup.addListener(() => {
  console.log('[Happy Scroll AI] Extension started');
});

// Message handler for communication with content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log('[Happy Scroll AI] Message received:', request);
  
  // Handle different message types
  if (request.type === 'VIDEO_SKIPPED') {
    console.log(`[Happy Scroll AI] Video skipped: ${request.videoId}`);
    // Could add notification or badge update here
  } else if (request.type === 'VIDEO_SAFE') {
    console.log(`[Happy Scroll AI] Video safe: ${request.videoId}`);
  } else if (request.type === 'API_ERROR') {
    console.error(`[Happy Scroll AI] API Error:`, request.error);
  }
  
  // Send response back to content script
  sendResponse({ success: true });
  return true; // Keep message channel open for async response
});

// Handle extension icon click (optional - can open options page or show popup)
chrome.action.onClicked.addListener((tab) => {
  console.log('[Happy Scroll AI] Extension icon clicked on tab:', tab.url);
  
  // Check if we're on a YouTube page
  if (tab.url && tab.url.includes('youtube.com')) {
    console.log('[Happy Scroll AI] Already on YouTube - monitoring active');
  } else {
    console.log('[Happy Scroll AI] Navigate to YouTube Shorts to use the extension');
  }
});

console.log('[Happy Scroll AI] Background service worker loaded');
