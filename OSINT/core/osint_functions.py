"""
Core OSINT functions - used by both GUI and Bot
"""
import requests
import re
import os
import json
from datetime import datetime
from typing import Dict, List, Optional

try:
    import instaloader
    INSTALOADER_AVAILABLE = True
except ImportError:
    INSTALOADER_AVAILABLE = False

# ---------- Telegram ----------
def search_telegram(identifier: str, identifier_type: str = "username") -> Dict:
    """
    Search Telegram by username or phone.
    Returns: {"success": bool, "message": str, "data": dict}
    """
    if identifier_type == "username":
        if not identifier.startswith("@"):
            username = identifier
        else:
            username = identifier[1:]
        
        url = f"https://t.me/{username}"
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200 and "tgme_page_title" in resp.text:
                # Extract profile info
                name_match = re.search(r'<meta property="og:title" content="([^"]+)"', resp.text)
                desc_match = re.search(r'<meta property="og:description" content="([^"]+)"', resp.text)
                photo_match = re.search(r'<meta property="og:image" content="([^"]+)"', resp.text)
                
                name = name_match.group(1).strip() if name_match else username
                desc = desc_match.group(1).strip() if desc_match else ""
                photo = photo_match.group(1).strip() if photo_match else ""
                
                return {
                    "success": True,
                    "message": f"✅ Found: @{username} → {name}",
                    "data": {
                        "platform": "telegram",
                        "username": username,
                        "display_name": name,
                        "description": desc,
                        "photo_url": photo,
                        "profile_url": url,
                        "timestamp": datetime.now().isoformat()
                    }
                }
            elif resp.status_code == 404:
                return {
                    "success": False,
                    "message": f"❌ Not found: @{username}",
                    "data": {"platform": "telegram", "username": username}
                }
            else:
                return {
                    "success": False,
                    "message": f"❓ Status {resp.status_code}",
                    "data": {"platform": "telegram", "username": username}
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"⚠️ Network error: {e}",
                "data": {"platform": "telegram", "username": username}
            }
    
    elif identifier_type == "phone":
        # Telegram doesn't have public phone search, but we can note it
        return {
            "success": False,
            "message": f"⚠️ Telegram: Phone search not available publicly. Use username.",
            "data": {"platform": "telegram", "phone": identifier}
        }
    
    return {"success": False, "message": "Invalid identifier type", "data": {}}

# ---------- Instagram ----------
def search_instagram(identifier: str, identifier_type: str = "username") -> Dict:
    """
    Search Instagram by username.
    Returns: {"success": bool, "message": str, "data": dict}
    """
    if identifier_type != "username":
        return {
            "success": False,
            "message": "Instagram requires username",
            "data": {}
        }
    
    username = identifier.lstrip("@")
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200 and "profilePage_" in resp.text:
            # Extract profile info
            full_match = re.search(r'"full_name":"([^"]+)"', resp.text)
            bio_match = re.search(r'"biography":"([^"]+)"', resp.text)
            posts_match = re.search(r'"edge_owner_to_timeline_media":{"count":(\d+)}', resp.text)
            followers_match = re.search(r'"edge_followed_by":{"count":(\d+)}', resp.text)
            following_match = re.search(r'"edge_follow":{"count":(\d+)}', resp.text)
            
            full = full_match.group(1) if full_match else "Unknown"
            bio = bio_match.group(1) if bio_match else ""
            posts = posts_match.group(1) if posts_match else "0"
            followers = followers_match.group(1) if followers_match else "0"
            following = following_match.group(1) if following_match else "0"
            
            return {
                "success": True,
                "message": f"✅ Found: @{username} → {full} ({followers} followers)",
                "data": {
                    "platform": "instagram",
                    "username": username,
                    "full_name": full,
                    "bio": bio,
                    "posts": posts,
                    "followers": followers,
                    "following": following,
                    "profile_url": url,
                    "timestamp": datetime.now().isoformat()
                }
            }
        elif resp.status_code == 404:
            return {
                "success": False,
                "message": f"❌ Profile not found: @{username}",
                "data": {"platform": "instagram", "username": username}
            }
        elif "login" in resp.url:
            return {
                "success": False,
                "message": f"🔒 Private account: @{username}",
                "data": {"platform": "instagram", "username": username, "private": True}
            }
        else:
            return {
                "success": False,
                "message": f"❓ Could not verify (status {resp.status_code})",
                "data": {"platform": "instagram", "username": username}
            }
    except Exception as e:
        return {
            "success": False,
            "message": f"⚠️ Network error: {e}",
            "data": {"platform": "instagram", "username": username}
        }

# ---------- Instagram Download ----------
def download_instagram_posts(username: str, max_posts: int = 10) -> Dict:
    """Download posts using Instaloader"""
    if not INSTALOADER_AVAILABLE:
        return {
            "success": False,
            "message": "❌ Instaloader not installed",
            "data": {}
        }
    
    try:
        loader = instaloader.Instaloader(
            download_pictures=True,
            download_videos=True,
            download_video_thumbnails=False,
            save_metadata=False,
            compress_json=False,
            filename_pattern='{date_utc}_UTC_{typename}',
            dirname_pattern=f'downloads/{username}'
        )
        
        profile = instaloader.Profile.from_username(loader.context, username)
        count = 0
        
        for post in profile.get_posts():
            if count >= max_posts:
                break
            loader.download_post(post, target=profile.username)
            count += 1
        
        return {
            "success": True,
            "message": f"✅ Downloaded {count} posts from @{username}",
            "data": {
                "count": count,
                "path": f"downloads/{username}",
                "timestamp": datetime.now().isoformat()
            }
        }
        
    except instaloader.exceptions.ProfileNotExistsException:
        return {"success": False, "message": f"❌ Profile @{username} does not exist.", "data": {}}
    except instaloader.exceptions.PrivateProfileNotFollowedException:
        return {"success": False, "message": f"🔒 Private profile - needs login.", "data": {}}
    except Exception as e:
        return {"success": False, "message": f"⚠️ Error: {e}", "data": {}}

# ---------- Iranian Apps (Placeholders) ----------
def search_soroush(identifier: str, identifier_type: str = "username") -> Dict:
    return {
        "success": False,
        "message": "[Soroush] No public API available",
        "data": {"platform": "soroush", identifier_type: identifier}
    }

def search_bale(identifier: str, identifier_type: str = "username") -> Dict:
    return {
        "success": False,
        "message": "[Bale] No public API available",
        "data": {"platform": "bale", identifier_type: identifier}
    }

def search_rubika(identifier: str, identifier_type: str = "username") -> Dict:
    return {
        "success": False,
        "message": "[Rubika] No public API available",
        "data": {"platform": "rubika", identifier_type: identifier}
    }

# ---------- Universal Search ----------
def search_all_platforms(identifier: str, platforms: List[str], identifier_type: str = "auto") -> List[Dict]:
    """
    Search one identifier across multiple platforms.
    identifier_type: "auto", "username", "phone", "name"
    """
    # Auto-detect type
    if identifier_type == "auto":
        if identifier.startswith("+") or (identifier.replace(" ", "").isdigit() and len(identifier) > 8):
            identifier_type = "phone"
        elif identifier.startswith("@") or (" " not in identifier and "." in identifier):
            identifier_type = "username"
        else:
            identifier_type = "name"
    
    platform_functions = {
        "telegram": search_telegram,
        "instagram": search_instagram,
        "soroush": search_soroush,
        "bale": search_bale,
        "rubika": search_rubika
    }
    
    results = []
    for platform in platforms:
        if platform in platform_functions:
            result = platform_functions[platform](identifier, identifier_type)
            results.append(result)
    
    return results
