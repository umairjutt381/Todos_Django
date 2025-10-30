# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# import json
# import time
#
# chrome_options = Options()
# chrome_options.add_argument("--headless=new")
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
#
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
# driver.set_script_timeout(60)
#
# driver.get("https://www.w3schools.com")
# time.sleep(5)
#
#
# script = """
# const done = arguments[0];
# (async () => {
#   try {
#     const dbs = await indexedDB.databases();
#     if (!dbs.length) {
#       done({ status: "no_databases", data: [] });
#       return;
#     }
#
#     const result = {};
#     let pending = dbs.length;
#     for (const dbInfo of dbs) {
#       const name = dbInfo.name;
#       if (!name) {
#         if (--pending === 0) done({ status: "ok", data: result });
#         continue;
#       }
#
#       const request = indexedDB.open(name);
#       request.onsuccess = event => {
#         const db = event.target.result;
#         const stores = Array.from(db.objectStoreNames);
#         result[name] = {};
#
#         if (!stores.length) {
#           if (--pending === 0) done({ status: "ok", data: result });
#           return;
#         }
#
#         let storePending = stores.length;
#         stores.forEach(storeName => {
#           const tx = db.transaction(storeName, "readonly");
#           const store = tx.objectStore(storeName);
#           const getAll = store.getAll();
#           getAll.onsuccess = () => {
#             result[name][storeName] = getAll.result;
#             if (--storePending === 0 && --pending === 0) done({ status: "ok", data: result });
#           };
#           getAll.onerror = () => {
#             result[name][storeName] = { error: "read_failed" };
#             if (--storePending === 0 && --pending === 0) done({ status: "ok", data: result });
#           };
#         });
#       };
#       request.onerror = () => {
#         result[name] = { error: "open_failed" };
#         if (--pending === 0) done({ status: "ok", data: result });
#       };
#     }
#   } catch (err) {
#     done({ status: "error", message: err.message });
#   }
# })();
# """
#
# data = driver.execute_async_script(script)
#
# print("\n=== IndexedDB Data ===")
# print(json.dumps(data, indent=4))
#
# driver.quit()
