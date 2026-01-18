# File Upload Skill

Upload local files to websites without triggering native file picker dialogs. Uses JavaScript DataTransfer API to programmatically set files on input elements.

## Triggers

- "upload [file] to this page"
- "attach my CV/resume"
- "upload file to this form"
- "select file for upload"
- When user needs to upload a file to a website

## Workflow

### Step 1: Get file path and target

Ask the user if not provided:
- **File path**: The local file to upload (e.g., `/Users/terry/Documents/resume.pdf`)
- **Target element** (optional): Specific file input to target if multiple exist

### Step 2: Get browser context

```
Use mcp__claude-in-chrome__tabs_context_mcp to get current tab
```

### Step 3: Find file input elements

```
Use mcp__claude-in-chrome__find with query "file input or upload button"
```

If multiple file inputs found, ask user which one to use or use the most relevant based on context.

### Step 4: Read and encode the local file

```bash
# Get file info
FILE_PATH="/path/to/file.pdf"
FILE_NAME=$(basename "$FILE_PATH")
FILE_SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH")

# Get MIME type
case "${FILE_NAME##*.}" in
  pdf) MIME_TYPE="application/pdf" ;;
  doc) MIME_TYPE="application/msword" ;;
  docx) MIME_TYPE="application/vnd.openxmlformats-officedocument.wordprocessingml.document" ;;
  txt) MIME_TYPE="text/plain" ;;
  png) MIME_TYPE="image/png" ;;
  jpg|jpeg) MIME_TYPE="image/jpeg" ;;
  gif) MIME_TYPE="image/gif" ;;
  *) MIME_TYPE="application/octet-stream" ;;
esac

# Encode to base64
BASE64_CONTENT=$(base64 -i "$FILE_PATH")
```

### Step 5: Inject file using JavaScript DataTransfer API

Use `mcp__claude-in-chrome__javascript_tool` to execute:

```javascript
(async function() {
  // File details (injected by Claude)
  const fileName = "FILENAME_HERE";
  const mimeType = "MIME_TYPE_HERE";
  const base64Content = "BASE64_CONTENT_HERE";

  // Decode base64 to binary
  const binaryString = atob(base64Content);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }

  // Create File object
  const file = new File([bytes], fileName, { type: mimeType });

  // Create DataTransfer and add file
  const dataTransfer = new DataTransfer();
  dataTransfer.items.add(file);

  // Find target file input (use ref if provided, otherwise first file input)
  const fileInput = document.querySelector('INPUT_SELECTOR_HERE');

  if (!fileInput) {
    return "ERROR: No file input found";
  }

  // Set files on input
  fileInput.files = dataTransfer.files;

  // Dispatch events to notify the page
  fileInput.dispatchEvent(new Event('change', { bubbles: true }));
  fileInput.dispatchEvent(new Event('input', { bubbles: true }));

  // Some sites use drag-drop handlers, trigger those too
  const dropEvent = new DragEvent('drop', {
    bubbles: true,
    dataTransfer: dataTransfer
  });
  fileInput.dispatchEvent(dropEvent);

  return `SUCCESS: Uploaded "${fileName}" (${file.size} bytes) to file input`;
})();
```

### Step 6: Verify upload

Take a screenshot to confirm the file was attached:
```
Use mcp__claude-in-chrome__computer with action "screenshot"
```

Look for:
- File name displayed on the page
- Upload progress indicator
- Preview of the uploaded file
- Any error messages

### Step 7: Report result

Tell the user:
- Whether upload succeeded
- File name and size that was uploaded
- Any next steps (e.g., "Click Submit to complete the application")

## Handling Edge Cases

### Multiple file inputs
Ask user: "I found X file inputs on this page. Which one should I use?"
- List them with descriptions
- Let user choose by number or description

### Drag-drop only upload zones
Some sites don't use `<input type="file">` but only accept drag-drop. For these:
1. Find the drop zone element
2. Dispatch dragenter, dragover, and drop events with the DataTransfer object

### File size limits
Before uploading, check if the site shows a file size limit. Warn user if file exceeds it.

### File type restrictions
Check the input's `accept` attribute. Warn if file type doesn't match.

```javascript
const acceptedTypes = fileInput.getAttribute('accept');
if (acceptedTypes && !acceptedTypes.includes(mimeType) && !acceptedTypes.includes('*')) {
  return `WARNING: This input only accepts ${acceptedTypes}, but your file is ${mimeType}`;
}
```

## Common File Paths (Terry's files)

- CV: `/Users/terry/Library/Mobile Documents/com~apple~CloudDocs/Terry_Li_CV_2026-01-10.pdf`
- Notes: `/Users/terry/notes/`

## Example Usage

**User**: "Upload my CV to this job application"

**Claude**:
1. Gets current tab (job application page)
2. Finds file input for resume/CV
3. Reads CV from iCloud path
4. Injects using DataTransfer
5. Takes screenshot to confirm
6. "Done! Your CV has been attached. Click 'Submit Application' to complete."

## Limitations

- Cannot upload to sites that require server-side file validation before accepting
- Some sites may detect programmatic uploads and reject them
- Very large files (>50MB) may cause browser memory issues with base64 encoding
- Sites using complex upload widgets (like Dropbox Chooser) may not work

## Why This Works

The native file picker dialog is an OS-level security feature. However:
- The browser's File API allows creating File objects programmatically
- DataTransfer API (designed for drag-drop) can set files on inputs
- This is the same approach Selenium and other automation tools use
- It's not a security bypass - we're using legitimate browser APIs
