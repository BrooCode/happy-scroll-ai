/**
 * Happy Scroll AI - Content Script
 * 
 * This script runs on YouTube pages and automatically skips unsafe YouTube Shorts
 * by calling the Happy Scroll AI API to check video safety.
 * 
 * Rate Limiting: 8 videos per day per user (demo version)
 */

// Configuration
const API_ENDPOINT = 'https://happy-scroll-service-zjehvyppna-uc.a.run.app/api/happyScroll/v1/verdict';
const PAGE_LOAD_DELAY = 2000; // 2 seconds delay before checking
const NEXT_BUTTON_SELECTORS = [
  'button[aria-label="Next video"]',
  'button[aria-label="Next"]',
  '.navigation-button.style-scope.ytd-shorts'
];

// Rate limiting configuration
const MAX_VIDEOS_PER_DAY = 8;
const STORAGE_KEY = 'happyscroll_video_count';
const STORAGE_DATE_KEY = 'happyscroll_last_reset';

// State management
let isProcessing = false;
let lastCheckedUrl = null;

/**
 * Check video limit for rate limiting
 */
async function checkVideoLimit() {
  const today = new Date().toDateString();
  const stored = await chrome.storage.local.get([STORAGE_KEY, STORAGE_DATE_KEY]);
  
  // Reset counter if it's a new day
  if (stored[STORAGE_DATE_KEY] !== today) {
    await chrome.storage.local.set({
      [STORAGE_KEY]: 0,
      [STORAGE_DATE_KEY]: today
    });
    return { allowed: true, count: 0 };
  }
  
  const count = stored[STORAGE_KEY] || 0;
  
  if (count >= MAX_VIDEOS_PER_DAY) {
    return { allowed: false, count };
  }
  
  return { allowed: true, count };
}

/**
 * Increment video count after successful check
 */
async function incrementVideoCount() {
  const stored = await chrome.storage.local.get([STORAGE_KEY]);
  const count = (stored[STORAGE_KEY] || 0) + 1;
  await chrome.storage.local.set({ [STORAGE_KEY]: count });
  return count;
}

/**
 * Show rate limit message to user
 */
function showLimitMessage() {
  // Remove any existing banner
  const existingBanner = document.getElementById('happyscroll-limit-banner');
  if (existingBanner) {
    existingBanner.remove();
  }

  // Create a banner on the page
  const banner = document.createElement('div');
  banner.id = 'happyscroll-limit-banner';
  banner.style.cssText = +""+
    position: fixed;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 20px 40px;
    border-radius: 12px;
    box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    z-index: 10000;
    font-family: 'YouTube Sans', 'Roboto', Arial, sans-serif;
    text-align: center;
    max-width: 500px;
    animation: slideDown 0.3s ease-out;
  +""+;
  banner.innerHTML = +""+
    <div style="font-size: 24px; margin-bottom: 8px;"></div>
    <strong style="font-size: 18px; display: block; margin-bottom: 8px;">Happy Scroll AI - Daily Limit Reached</strong>
    <span style="font-size: 14px; opacity: 0.9;">
      You've checked  videos today.<br>
      Come back tomorrow for more safe browsing! 
    </span>
    <div style="margin-top: 12px; font-size: 12px; opacity: 0.7;">
      This is a demo project with limited free API usage.
    </div>
  +""+;
  
  // Add animation
  const style = document.createElement('style');
  style.textContent = +""+
    @keyframes slideDown {
      from {
        opacity: 0;
        transform: translateX(-50%) translateY(-20px);
      }
      to {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
      }
    }
  +""+;
  document.head.appendChild(style);
  
  document.body.appendChild(banner);
  
  setTimeout(() => {
    banner.style.transition = 'opacity 0.3s ease-out';
    banner.style.opacity = '0';
    setTimeout(() => banner.remove(), 300);
  }, 6000);
}

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
 * Fetch safety verdict from API with rate limiting
 */
async function checkVideoSafety(videoId) {
  // Check limit first
  const limitCheck = await checkVideoLimit();
  
  if (!limitCheck.allowed) {
    console.log(+""+[Happy Scroll AI]  Daily limit reached (/ videos)+""+);
    showLimitMessage();
    return null; // Don't check the video
  }
  
  try {
    console.log(+""+[Happy Scroll AI]  Checking video safety (/)...+""+);
    console.log(+""+[Happy Scroll AI] Checking safety for video: +""+);
    
    const videoUrl = +""+https://www.youtube.com/watch?v=+""+;
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
      const errorText = await response.text();
      console.error(+""+[Happy Scroll AI]  API Error :+""+, errorText);
      
      // Handle rate limit from backend
      if (response.status === 429) {
        showLimitMessage();
      }
      
      return null;
    }

    const data = await response.json();
    console.log('[Happy Scroll AI] API Response:', data);
    
    // Increment counter after successful API call
    const newCount = await incrementVideoCount();
    console.log(+""+[Happy Scroll AI]  Videos checked today: /+""+);
    
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

    // If null is returned, rate limit was hit or error occurred
    if (verdict === null) {
      console.log('[Happy Scroll AI]  Skipping check - rate limit or error');
    } else if (verdict.is_safe === false) {
      console.log(+""+[Happy Scroll AI]  UNSAFE VIDEO DETECTED - Skipping to next Short+""+);
      console.log(+""+[Happy Scroll AI] Reason: +""+);
      
      // Skip to next video
      clickNextButton();
    } else if (verdict.is_safe === true) {
      console.log(+""+[Happy Scroll AI]  Video is SAFE - Continuing playback+""+);
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
  console.log(+""+[Happy Scroll AI]  Rate limit:  videos per day+""+);

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
