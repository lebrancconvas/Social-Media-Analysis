import json  
from playwright.sync_api import sync_playwright  

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

SOCIAL_BLADE_BASE_URL = "https://socialblade.com/"
TOP_100_YOUTUBER = "youtube/lists/top/100/subscribers/all/global"  

# Get the handle users from argument of top.  
def get_handles(url: str):
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(locale="en-US", user_agent=USER_AGENT)
    page = context.new_page()

    page.goto(url)

    CHANNEL_HANDLE_SELECTOR = "tbody > tr > td > a"   
    # print(f"[LOG] Experiment with selector: {CHANNEL_HANDLE_SELECTOR}\n")  

    channel_handle_raw = page.locator(CHANNEL_HANDLE_SELECTOR).all()
    channel_handle_url = list(map(lambda username: username.get_attribute("href"), channel_handle_raw))
    
    channel_handles = []

    for channel_handle in channel_handle_url:
      if channel_handle not in channel_handles:
        channel_handles.append(channel_handle)
    
    return list(map(lambda handle: handle.split("/")[-1], channel_handles))   

def convert_to_number(str_value: str) -> int:
  if "M" in str_value or "m" in str_value:
    return int(str_value[:-1]) * 1_000_000
  elif "K" in str_value or "k" in str_value:
    return int(str_value[:-1]) * 1_000
  elif "B" in str_value or "b" in str_value:
    return int(str_value[:-1]) * 1_000_000_000
  else:
    return int(str_value)
  return 0

def get_information(handle_username: str):
  with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(locale="en-US", user_agent=USER_AGENT)
    page = context.new_page()

    url = f"https://socialblade.com/youtube/handle/{handle_username}"

    page.goto(url)

    CHANNEL_NAME_SELECTOR = "#__next > div > div.w-full.flex-1.flex-col.flex > div.mx-auto.flex-1.h-full.w-full.flex.pt-20.md\:pt-24.z-20 > div.lg\:pl-72.flex-1.flex-col.w-full.overflow-y-auto.overflow-x-hidden.flex > div.flex-1.relative > div > div.bg-secondary-700.dark\:bg-primary-800.text-white.shadow-md.overflow-hidden > div.bg-secondary-500.dark\:bg-primary-900.mx-auto.my-0.flex.flex-col.md\:flex-row.relative.transform.motion-safe\:transition-\[margin-top\].motion-safe\:duration-300 > div.flex.flex-row.w-full.container.my-0.mx-auto.px-6 > div.flex.flex-1.flex-col.md\:flex-row.gap-5.lg\:gap-0.lg\:items-center.my-3\.5.ml-2\.5.lg\:ml-0.lg\:block.lg\:mb-0.lg\:-mt-6.lg\:pl-3\.5.text-xl.max-w-\[calc\(100\%-100px\)\] > div.flex.flex-row.flex-1.p-0.mr-2\.5.lg\:flex-0.lg\:-mt-2.lg\:mr-0.h-full.lg\:h-7.gap-2\.5.md\:items-center > h3 > span.truncate.max-w-full"
    SUBSCRIBER_SELECTOR = "#__next > div > div.w-full.flex-1.flex-col.flex > div.mx-auto.flex-1.h-full.w-full.flex.pt-20.md\:pt-24.z-20 > div.lg\:pl-72.flex-1.flex-col.w-full.overflow-y-auto.overflow-x-hidden.flex > div.flex-1.relative > div > div.bg-secondary-700.dark\:bg-primary-800.text-white.shadow-md.overflow-hidden > div.grid.lg\:hidden.text-center.grid-cols-2.md\:grid-cols-4.bg-secondary-500.dark\:bg-primary-900.dark\:border-t-primary-600.py-2\.5.gap-y-2\.5 > div:nth-child(1) > p:nth-child(2)"
    VIEW_SELECTOR = "#__next > div > div.w-full.flex-1.flex-col.flex > div.mx-auto.flex-1.h-full.w-full.flex.pt-20.md\:pt-24.z-20 > div.lg\:pl-72.flex-1.flex-col.w-full.overflow-y-auto.overflow-x-hidden.flex > div.flex-1.relative > div > div.bg-secondary-700.dark\:bg-primary-800.text-white.shadow-md.overflow-hidden > div.grid.lg\:hidden.text-center.grid-cols-2.md\:grid-cols-4.bg-secondary-500.dark\:bg-primary-900.dark\:border-t-primary-600.py-2\.5.gap-y-2\.5 > div:nth-child(2) > p:nth-child(2)"
    NUMBER_OF_VIDEO_SELECTOR = "#__next > div > div.w-full.flex-1.flex-col.flex > div.mx-auto.flex-1.h-full.w-full.flex.pt-20.md\:pt-24.z-20 > div.lg\:pl-72.flex-1.flex-col.w-full.overflow-y-auto.overflow-x-hidden.flex > div.flex-1.relative > div > div.bg-secondary-700.dark\:bg-primary-800.text-white.shadow-md.overflow-hidden > div.bg-secondary-500.dark\:bg-primary-900.mx-auto.my-0.flex.flex-col.md\:flex-row.relative.transform.motion-safe\:transition-\[margin-top\].motion-safe\:duration-300 > div.flex.flex-row.w-full.container.my-0.mx-auto.px-6 > div.flex.flex-1.flex-col.md\:flex-row.gap-5.lg\:gap-0.lg\:items-center.my-3\.5.ml-2\.5.lg\:ml-0.lg\:block.lg\:mb-0.lg\:-mt-6.lg\:pl-3\.5.text-xl.max-w-\[calc\(100\%-100px\)\] > div.hidden.md\:flex > div.hidden.lg\:block.flex-1.outline-hidden.pb-1 > div > div:nth-child(3) > p.text-\[1\.25em\].font-extralight.pr-\[50px\]"
    DATE_CREATED_SELECTOR = "#__next > div > div.w-full.flex-1.flex-col.flex > div.mx-auto.flex-1.h-full.w-full.flex.pt-20.md\:pt-24.z-20 > div.lg\:pl-72.flex-1.flex-col.w-full.overflow-y-auto.overflow-x-hidden.flex > div.flex-1.relative > div > div.bg-secondary-700.dark\:bg-primary-800.text-white.shadow-md.overflow-hidden > div.grid.lg\:hidden.text-center.grid-cols-2.md\:grid-cols-4.bg-secondary-500.dark\:bg-primary-900.dark\:border-t-primary-600.py-2\.5.gap-y-2\.5 > div:nth-child(4) > p:nth-child(2)"

    channel_name_data = page.get_by_text(CHANNEL_NAME_SELECTOR).inner_text()
    subscriber_data = page.get_by_text("Subscribers").inner_text()  
    view_data = page.get_by_text("Views").inner_text()
    number_of_video_data = page.get_by_text("Videos").inner_text()
    date_created_data = page.get_by_text("Created On").inner_text()

    data = {
      "handle": handle_username,
      "channel": channel_name_data,
      "subscriber": convert_to_number(subscriber_data),
      "total_view": convert_to_number(view_data),
      "number_of_video": convert_to_number(number_of_video_data),
      "date_created": date_created_data 
    }   
    
    return data  
      
def run():
  top_100_youtubers = []

  top_100_youtuber_handles = get_handles("https://socialblade.com/youtube/lists/top/100/subscribers/all/global")

  for handle in top_100_youtuber_handles:
    info = get_information(handle)
    top_100_youtubers.append(info)
    print(f"[LOG] Success: Process Information from @{handle} success.\nInformation: {info}")
  
  with open("./data/json/top_100_youtubers_social_blade.json", "w", encoding="utf-8") as json_file:
    json_data = json.dumps(top_100_youtubers, indent=4, ensure_ascii=False)
    json_file.write(json_data)

if __name__ == "__main__":  
  run()