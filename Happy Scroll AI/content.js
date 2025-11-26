/**
 * Happy Scroll AI - Content Script
 * 
 * This script runs on YouTube pages and automatically skips unsafe YouTube Shorts
 * by calling the Happy Scroll AI API to check video safety.
 */

// Configuration
const API_ENDPOINT = 'https://happy-scroll-service-zjehvyppna-uc.a.run.app/api/happyScroll/v1/verdict';
const PAGE_LOAD_DELAY = 2000; // 2 seconds delay before checking
const NEXT_BUTTON_SELECTORS = [
  'button[aria-label="Next video"]',
  'button[aria-label="Next"]',
  '.navigation-button.style-scope.ytd-shorts'
];

// State management
let isProcessing = false;
let lastCheckedUrl = null;

/**
 * Extract video ID from YouTube Shorts URL
 */
function getVideoIdFromUrl(url) {
  const match = url.match(/\/shorts\/([a-zA-Z0-9_-]+)/);
  return match ? match[1] : null;
}

/**
 * Check if current page is a YouTube Shorts page
 */
function isYouTubeShorts() {
  return window.location.pathname.includes('/shorts/');
}

/**
 * Fetch safety verdict from API
 */
async function checkVideoSafety(videoId) {
  try {
    console.log(`[Happy Scroll AI] Checking safety for video: ${videoId}`);
    
    const videoUrl = `https://www.youtube.com/watch?v=${videoId}`;
    const response = await fetch(API_ENDPOINT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        video_url: videoUrl
      })
    });

    if (!response.ok) {
      console.error(`[Happy Scroll AI] API error: ${response.status} ${response.statusText}`);
      return null;
    }

    const data = await response.json();
    console.log('[Happy Scroll AI] API Response:', data);
    
    return data;
  } catch (error) {
    console.error('[Happy Scroll AI] Failed to check video safety:', error);
    return null;
  }
}

/**
 * Find and click the "Next" button to skip to next Short
 */
function clickNextButton() {
  for (const selector of NEXT_BUTTON_SELECTORS) {
    const nextButton = document.querySelector(selector);
    if (nextButton) {
      console.log('[Happy Scroll AI] Clicking Next button...');
      nextButton.click();
      return true;
    }
  }
  
  console.warn('[Happy Scroll AI] Next button not found');
  return false;
}

/**
 * Main function to check and skip unsafe videos
 */
async function checkAndSkipIfUnsafe() {
  // Only process YouTube Shorts pages
  if (!isYouTubeShorts()) {
    return;
  }

  // Prevent multiple simultaneous checks
  if (isProcessing) {
    return;
  }

  const currentUrl = window.location.href;
  const videoId = getVideoIdFromUrl(currentUrl);

  // Skip if no video ID or already checked this video
  if (!videoId || currentUrl === lastCheckedUrl) {
    return;
  }

  isProcessing = true;
  lastCheckedUrl = currentUrl;

  try {
    // Wait for page to fully load
    await new Promise(resolve => setTimeout(resolve, PAGE_LOAD_DELAY));

    // Check video safety
    const verdict = await checkVideoSafety(videoId);

    if (verdict && verdict.is_safe === false) {
      console.log(`[Happy Scroll AI] ⚠️ UNSAFE VIDEO DETECTED - Skipping to next Short`);
      console.log(`[Happy Scroll AI] Reason: ${verdict.reasons || 'No reason provided'}`);
      
      // Skip to next video
      clickNextButton();
    } else if (verdict && verdict.is_safe === true) {
      console.log(`[Happy Scroll AI] ✅ Video is SAFE - Continuing playback`);
    } else {
      console.log(`[Happy Scroll AI] ⚠️ Unable to determine safety - Allowing video`);
    }
  } catch (error) {
    console.error('[Happy Scroll AI] Error during safety check:', error);
  } finally {
    isProcessing = false;
  }
}

/**
 * Initialize the extension
 */
function initialize() {
  console.log('[Happy Scroll AI] Extension initialized');

  // Check on initial load
  if (isYouTubeShorts()) {
    checkAndSkipIfUnsafe();
  }

  // Monitor URL changes (YouTube is a Single Page Application)
  let lastUrl = location.href;
  new MutationObserver(() => {
    const currentUrl = location.href;
    if (currentUrl !== lastUrl) {
      lastUrl = currentUrl;
      console.log('[Happy Scroll AI] URL changed:', currentUrl);
      
      // Reset state for new video
      lastCheckedUrl = null;
      isProcessing = false;
      
      // Check new video
      if (isYouTubeShorts()) {
        checkAndSkipIfUnsafe();
      }
    }
  }).observe(document, { subtree: true, childList: true });

  console.log('[Happy Scroll AI] Monitoring YouTube Shorts for unsafe content...');
}

// Start the extension when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initialize);
} else {
  initialize();
}
