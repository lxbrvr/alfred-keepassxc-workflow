ObjC.import("AppKit")


function* integerIncrementer(start, end) {
	while (start <= end) {
		yield start++
	}
}


function run(argv) {
	let userValueForClipboard = argv[0]
	let utf8PlainTextType = "public.utf8-plain-text"
	let userTimeout = parseInt(argv[1])
	let pasteBoard = $.NSPasteboard.generalPasteboard

	pasteBoard.clearContents
	pasteBoard.setStringForType('', 'org.nspasteboard.ConcealedType')  //http://nspasteboard.org
	pasteBoard.setStringForType(userValueForClipboard, utf8PlainTextType)

	if (!userTimeout) {
		return
	}

	let maxTimeout = 999  // the same limit in KeepassXC UI.
	let timeout = userTimeout > maxTimeout? maxTimeout: userTimeout
	let latestCopiedValue = userValueForClipboard

	for (let i of integerIncrementer(1, timeout)) {
		delay(1)

		let actualValueFromClipboard = ObjC.unwrap(pasteBoard.stringForType(utf8PlainTextType))
		let isRelevantValueInClipboard = latestCopiedValue === actualValueFromClipboard

		if (!isRelevantValueInClipboard) {
			break
		}

		let isLatestIteration = i === timeout

		if (isLatestIteration && isRelevantValueInClipboard) {
			pasteBoard.clearContents
		}
	}
}

