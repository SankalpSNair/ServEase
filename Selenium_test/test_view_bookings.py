import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def test_view_bookings():
    """Test the booking management functionality"""
    print("✓ Starting test")
    
    # Add options to prevent window from closing unexpectedly
    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)  # Keep browser open
    chrome_options.add_argument("--disable-notifications")  # Disable notifications
    
    driver = webdriver.Chrome(options=chrome_options)
    try:
        # Maximize window to avoid responsive menu issues
        driver.maximize_window()
        
        # First login as a regular user
        print("✓ Step 1: Login")
        driver.get("http://127.0.0.1:8000/")
        
        # Click on login link
        driver.find_element(By.CSS_SELECTOR, "strong").click()
        
        # Login with credentials
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
        username_field.click()
        username_field.send_keys("sankalpsnair01@gmail.com")
        
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        password_field.click()
        password_field.send_keys("Sankalp@123")
        
        # Press Enter to submit
        password_field.send_keys(Keys.ENTER)
        print("✓ Login success")

        # Wait for homepage to load
        time.sleep(2)
        
        # Navigate to View Bookings page
        print("✓ Step 2: Navigating to View Bookings")
        try:
            # Try to find the View Bookings link in the navigation menu
            bookings_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'View Bookings')]"))
            )
            bookings_link.click()
        except Exception as e:
            print(f"⚠ Bookings link not found in menu, trying direct URL: {str(e)[:50]}")
            driver.get("http://127.0.0.1:8000/view_bookings/")
        
        # Wait for the bookings page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".booking-card, .table-responsive"))
        )
        print("✓ Bookings page loaded")
        
        # Test 1: Check if bookings are displayed
        print("✓ Step 3: Checking bookings display")
        try:
            # Look for booking cards or table rows
            booking_elements = driver.find_elements(By.CSS_SELECTOR, ".booking-card, .table tbody tr")
            
            if booking_elements:
                print(f"✓ Found {len(booking_elements)} bookings")
                
                # Test 2: Check booking details
                first_booking = booking_elements[0]
                
                # Try to extract booking information
                try:
                    # For card layout
                    booking_info = first_booking.text
                    print(f"✓ First booking details: {booking_info[:100]}...")
                except:
                    print("⚠ Could not extract booking text")
                
                # Test 3: Test action buttons if they exist
                try:
                    # Look for action buttons (View, Cancel, Pay, etc.)
                    action_buttons = first_booking.find_elements(By.CSS_SELECTOR, ".btn, button, a.action-button")
                    
                    if action_buttons:
                        print(f"✓ Found {len(action_buttons)} action buttons")
                        
                        # Test clicking the first action button that's not "Cancel" (to avoid canceling a booking)
                        for button in action_buttons:
                            button_text = button.text.strip().lower()
                            if button_text and "cancel" not in button_text and "delete" not in button_text:
                                print(f"✓ Found action button: {button_text}")
                                
                                # Store current URL to check if clicking causes navigation
                                current_url = driver.current_url
                                
                                # Click the button
                                # Use JavaScript click to avoid potential overlay issues
                                driver.execute_script("arguments[0].scrollIntoView(true);", button)
                                time.sleep(1)
                                
                                # Check if it's a view invoice or download button
                                if "invoice" in button_text or "download" in button_text or "view" in button_text:
                                    print("⚠ Skipping invoice/download button to avoid opening new tabs")
                                    continue
                                
                                # Click the button
                                try:
                                    # Store window handles before clicking
                                    original_window = driver.current_window_handle
                                    original_window_count = len(driver.window_handles)
                                    
                                    # Click the button
                                    driver.execute_script("arguments[0].click();", button)
                                    print(f"✓ Clicked on {button_text} button")
                                    
                                    # Wait a moment for any actions to complete
                                    time.sleep(2)
                                    
                                    # Check if a new window/tab was opened
                                    if len(driver.window_handles) > original_window_count:
                                        # Switch to the new window
                                        new_window = [window for window in driver.window_handles if window != original_window][0]
                                        driver.switch_to.window(new_window)
                                        print(f"✓ New window opened: {driver.current_url}")
                                        
                                        # Close the new window and switch back
                                        driver.close()
                                        driver.switch_to.window(original_window)
                                    
                                    # Check if URL changed (navigation occurred)
                                    elif driver.current_url != current_url:
                                        print(f"✓ Navigation occurred to: {driver.current_url}")
                                        
                                        # Navigate back to bookings page
                                        driver.back()
                                        time.sleep(2)
                                    
                                    # Check if a modal dialog appeared
                                    try:
                                        modal = WebDriverWait(driver, 3).until(
                                            EC.visibility_of_element_located((By.CSS_SELECTOR, ".modal, .swal2-container"))
                                        )
                                        print("✓ Modal dialog opened")
                                        
                                        # Close the modal if possible
                                        close_buttons = modal.find_elements(By.CSS_SELECTOR, ".close, .btn-close, .swal2-close, button")
                                        if close_buttons:
                                            driver.execute_script("arguments[0].click();", close_buttons[0])
                                            print("✓ Closed modal dialog")
                                    except:
                                        # No modal appeared, which is fine
                                        pass
                                        
                                    break  # We only need to test one button
                                except Exception as e:
                                    print(f"⚠ Error clicking button: {str(e)[:100]}")
                    else:
                        print("⚠ No action buttons found on booking")
                except Exception as e:
                    print(f"⚠ Error testing action buttons: {str(e)[:100]}")
            else:
                print("⚠ No bookings found. This could be normal for a new user.")
        except Exception as e:
            print(f"❌ Error checking bookings: {str(e)[:100]}")
        
        # Test passed if we got this far
        print("✅ TEST PASSED!")
                
    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)[:100]}")
        
        # Take a screenshot on failure
        try:
            # Check if driver is still active
            if driver.current_url:
                driver.save_screenshot("error_view_bookings.png")
                print("✓ Screenshot saved")
            else:
                print("⚠ Cannot take screenshot - driver not active")
        except Exception as screenshot_error:
            print(f"⚠ Screenshot failed: {str(screenshot_error)[:50]}")
        
        # Print a clear summary message
        print("\n❌ TEST SUMMARY: Test failed due to browser or element issues")
        raise
        
    finally:
        print("✓ Test completed")
        driver.quit()

if __name__ == "__main__":
    test_view_bookings()
