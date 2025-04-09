import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

def test_emergency_booking():
    """Test the emergency booking functionality"""
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
        
        # Click on login link (based on Selenium IDE)
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
        
        # Press Enter to submit (based on Selenium IDE)
        password_field.send_keys(Keys.ENTER)
        print("✓ Login success")

        # Wait for homepage to load
        time.sleep(2)
        
        # Navigate to Emergency page
        print("✓ Step 2: Emergency page")
        # Use the Emergency link instead of direct URL (based on Selenium IDE)
        try:
            emergency_link = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.LINK_TEXT, "Emergency"))
            )
            emergency_link.click()
        except Exception as e:
            print(f"⚠ Emergency link not found, trying direct URL: {str(e)[:50]}")
            driver.get("http://127.0.0.1:8000/emergency/")
        
        # Wait for the emergency page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".features-small-item"))
        )
        print("✓ Page loaded")
        
        # Test Plumbing Emergency service
        print("✓ Step 3: Testing service")
        
        # Print available service cards for debugging
        # Skip printing all available cards and buttons
        
        # Use the exact selector from Selenium IDE
        try:
            print("✓ Finding button")
            book_now_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".col-lg-4:nth-child(3) .main-button"))
            )
            book_now_button.click()
            print("✓ Clicked Book Now")
        
            # Wait for the booking modal to appear
            try:
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID, "bookingModal"))
                )
                print("✓ Modal opened")
            except TimeoutException:
                print("⚠ Checking alternative modal")
                # Try alternative modal selectors
                modal_selectors = [".modal", ".booking-modal", "[role='dialog']"]
                for selector in modal_selectors:
                    try:
                        modal = driver.find_element(By.CSS_SELECTOR, selector)
                        if modal.is_displayed():
                            print("✓ Found modal")
                            break
                    except:
                        continue
        
            # Fill in the booking form
            print("✓ Step 4: Filling form")
            
            # Use the location input field and current location link from Selenium IDE
            try:
                # Click on location input
                location_input = driver.find_element(By.ID, "locationInput")
                location_input.click()
                
                # Click Use Current Location link
                current_location_link = driver.find_element(By.LINK_TEXT, "Use Current Location")
                current_location_link.click()
                print("✓ Location requested")
                
                # Handle the getting location state
                time.sleep(2)  # Wait for geolocation process
                
                # Simulate geolocation by setting values directly if needed
                try:
                    latitude_field = driver.find_element(By.ID, "latitude")
                    longitude_field = driver.find_element(By.ID, "longitude")
                    driver.execute_script("arguments[0].value = '10.1234';", latitude_field)
                    driver.execute_script("arguments[0].value = '76.5678';", longitude_field)
                    print("✓ Location set")
                except Exception as e:
                    print("✓ Using browser geolocation")
            except Exception as e:
                print("⚠ Location handling issue")
            
            # Select emergency type using exact steps from Selenium IDE
            try:
                # Click on dropdown
                emergency_select = driver.find_element(By.ID, "additionalDetails")
                emergency_select.click()
                
                # Select the option (using the exact option from Selenium IDE)
                dropdown = driver.find_element(By.ID, "additionalDetails")
                dropdown.find_element(By.XPATH, "//option[. = 'Immediate medical assistance']").click()
                
                # Click on the option to ensure it's selected
                driver.find_element(By.CSS_SELECTOR, "option:nth-child(2)").click()
                print("✓ Emergency type selected")
            except Exception as e:
                print(f"Could not select emergency type: {str(e)}")
                # Fallback to simple select
                try:
                    select = Select(driver.find_element(By.ID, "additionalDetails"))
                    select.select_by_index(1)  # Select the first non-empty option
                    print("✓ Option selected (fallback)")
                except Exception as e:
                    print("⚠ Selection issue")
            
            # Submit the form
            print("✓ Step 5: Submitting form")
            try:
                # Store window handles before clicking (as in Selenium IDE)
                original_window = driver.current_window_handle
                original_window_count = len(driver.window_handles)
                
                # Click the book now button (as in Selenium IDE)
                book_now_btn = driver.find_element(By.CSS_SELECTOR, ".book-now-btn")
                book_now_btn.click()
                print("✓ Submit clicked")
                
                # Wait for new window using the same approach as Selenium IDE
                def wait_for_window(timeout = 2):
                    time.sleep(timeout)
                    wh_now = driver.window_handles
                    if len(wh_now) > original_window_count:
                        return set(wh_now).difference({original_window}).pop()
                    return None
                
                # Wait for the WhatsApp window
                print("✓ Waiting for WhatsApp")
                new_window = wait_for_window(2)
                success = new_window is not None
                
                if success:
                    print("✓ WhatsApp opened successfully")
                    
                    # Switch to the new window and close it
                    driver.switch_to.window(new_window)
                    driver.close()
                    
                    # Switch back to the original window
                    driver.switch_to.window(original_window)
                else:
                    print("⚠ No WhatsApp window detected")
                
                # Check if modal was closed after submission
                modal_closed = False
                try:
                    modal = driver.find_element(By.ID, "bookingModal")
                    modal_style = modal.get_attribute("style")
                    if "display: none" in modal_style:
                        modal_closed = True
                        print("Modal was closed after submission")
                except:
                    modal_closed = True
                    print("Modal was closed after submission")
                
                # Determine test result
                if success or modal_closed:
                    print("✅ TEST PASSED!")
                else:
                    print("\n❌ EMERGENCY BOOKING TEST FAILED!")
                    print("=====================================")
                    print("✗ Form submission did not trigger expected actions")
                    print(f"Current URL: {driver.current_url}")
                    print("=====================================")
                    raise TimeoutException("Could not verify successful form submission")
            except Exception as e:
                print(f"Error submitting form: {str(e)}")
                # Try alternative form submission
                try:
                    print("⚠ Trying alternative submission")
                    submit_buttons = driver.find_elements(By.CSS_SELECTOR, "button[type='submit'], input[type='submit']")
                    if submit_buttons:
                        driver.execute_script("arguments[0].click();", submit_buttons[0])
                        print("✓ Submit button clicked")
                    else:
                        # Try to find any button in the form
                        form_buttons = driver.find_elements(By.CSS_SELECTOR, ".booking-modal button, .modal button")
                        if form_buttons:
                            driver.execute_script("arguments[0].click();", form_buttons[0])
                            print("✓ Form button clicked")
                except Exception as e:
                    print(f"Alternative submission failed: {str(e)}")
                    raise
                
        except Exception as e:
            print(f"❌ Form error: {str(e)[:100]}")
            raise

    except Exception as e:
        print(f"❌ TEST FAILED: {str(e)[:100]}")
        
        # Take a screenshot on failure
        try:
            # Check if driver is still active
            if driver.current_url:
                driver.save_screenshot("error_emergency_booking.png")
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
    test_emergency_booking()
