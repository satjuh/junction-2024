export function openDatabase() {
  return new Promise<IDBDatabase>((resolve, reject) => {
    const request = indexedDB.open('FileStorageDB', 1)

    request.onupgradeneeded = (event) => {
      // @ts-ignore
      const db = event.target.result
      // Create an object store named 'files' if it doesn't exist
      if (!db.objectStoreNames.contains('files')) {
        db.createObjectStore('files', { keyPath: 'url' })
      }
    }

    request.onsuccess = (event) => {
      // @ts-ignore
      const db = event.target.result
      resolve(db as IDBDatabase)
    }

    request.onerror = (event) => {
      // @ts-ignore
      reject(event.target.error)
    }
  })
}

async function fetchAndStoreFile(url: string, db: IDBDatabase) {
  try {
    // Fetch the file as a Blob
    const response = await fetch(url)
    const blob = await response.blob()

    // Store the Blob in IndexedDB
    const transaction = db.transaction(['files'], 'readwrite')
    const store = transaction.objectStore('files')

    const item = {
      url: url,
      blob: blob,
      timestamp: new Date().getTime()
    }

    const request = store.put(item)

    return new Promise<Blob>((resolve, reject) => {
      request.onsuccess = () => {
        resolve(blob)
      }

      request.onerror = (event) => {
        // @ts-ignore
        console.error('Error storing file:', event.target.error)
      }
    })
  } catch (error) {
    console.error('Error:', error)
  }
}

function getFile(url: string, db: IDBDatabase) {
  return new Promise<Blob>(async (resolve, reject) => {
    try {
      const transaction = db.transaction(['files'], 'readonly')
      const store = transaction.objectStore('files')
      const request = store.get(url)

      request.onsuccess = (event) => {
        // @ts-ignore
        const result = event.target.result
        if (result) {
          resolve(result.blob)
        } else {
          reject('File not found')
        }
      }

      request.onerror = (event) => {
        // @ts-ignore
        reject(event.target.error)
      }
    } catch (error) {
      reject(error)
    }
  })
}

export async function retrieveFile(url: string): Promise<Blob> {
  const db = await openDatabase()
  try {
    // Try to get the file from IndexedDB
    const blob = await getFile(url, db)
    return blob
  } catch (error) {
    // If the file is not found in IndexedDB
    if (error === 'File not found') {
      try {
        // Fetch the file, store it in IndexedDB, and return the Blob
        const blob = await fetchAndStoreFile(url, db)

        if (!blob) {
          throw new Error('File not found')
        }

        return blob
      } catch (fetchError) {
        // Handle any errors that occur during fetching and storing
        throw fetchError
      }
    } else {
      // Re-throw any other errors
      throw error
    }
  }
}
