ObjC.import("stdlib")


let app = Application.currentApplication()
app.includeStandardAdditions = true

const windowTitle = "Alfred KeepassXC"
const maskedPassword = "••••••••"
const alfredWorkflowBundleId = $.getenv("alfred_workflow_bundleid")
const cancelButton = "Cancel"
const yesButton = "Yes"
const noButton = "No"

let CancelError = new Error()
const cancelErrorNumber = -128 // macos error code for cancel
CancelError.errorNumber = cancelErrorNumber


function setTemporaryEnv(name, value) {
    $.setenv(name, value, 1)
}


function unsetTemporaryEnv(name) {
    $.unsetenv(name)
}


function getenv(envName) {
    try {
        return $.getenv(envName)
    } catch (e) {}

}


const EnvNames = Object.freeze({
    ALFRED_KEYWORD: "alfred_keyword",
    KEEPASSXC_DB_PATH: "keepassxc_db_path",
    KEEPASSXC_CLI_PATH: "keepassxc_cli_path",
    KEEPASSXC_KEYFILE_PATH: "keepassxc_keyfile_path",
    KEEPASSXC_MASTER_PASSWORD: "keepassxc_master_password",
    KEYCHAIN_ACCOUNT: "keychain_account",
    KEYCHAIN_SERVICE: "keychain_service",
    SHOW_ATTRIBUTE_VALUES: "show_attribute_values",
    SHOW_UNFILLED_ATTRIBUTES: "show_unfilled_attributes",
    DESIRED_ATTRIBUTES: "desired_attributes",
    SHOW_PASSWORDS: "show_passwords",
    ENTRY_DELIMITER: "entry_delimiter",
})


const Settings = {
    ALFRED_KEYWORD: getenv(EnvNames.ALFRED_KEYWORD),
    KEEPASSXC_DB_PATH: getenv(EnvNames.KEEPASSXC_DB_PATH),
    KEEPASSXC_CLI_PATH: getenv(EnvNames.KEEPASSXC_CLI_PATH),
    KEEPASSXC_KEYFILE_PATH: getenv(EnvNames.KEEPASSXC_KEYFILE_PATH),
    KEEPASSXC_MASTER_PASSWORD: getenv(EnvNames.KEEPASSXC_MASTER_PASSWORD),
    KEYCHAIN_ACCOUNT: getenv(EnvNames.KEYCHAIN_ACCOUNT),
    KEYCHAIN_SERVICE: getenv(EnvNames.KEYCHAIN_SERVICE),
    SHOW_ATTRIBUTE_VALUES: getenv(EnvNames.SHOW_ATTRIBUTE_VALUES),
    SHOW_UNFILLED_ATTRIBUTES: getenv(EnvNames.SHOW_UNFILLED_ATTRIBUTES),
    DESIRED_ATTRIBUTES: getenv(EnvNames.DESIRED_ATTRIBUTES),
    SHOW_PASSWORDS: getenv(EnvNames.SHOW_PASSWORDS),
    ENTRY_DELIMITER: getenv(EnvNames.ENTRY_DELIMITER),
}


const DefaultEnvValues = {
    [EnvNames.ALFRED_KEYWORD]: "kp",
    [EnvNames.KEEPASSXC_DB_PATH]: "",
    [EnvNames.KEEPASSXC_CLI_PATH]: "/usr/local/bin/keepassxc-cli",
    [EnvNames.KEEPASSXC_KEYFILE_PATH]: "",
    [EnvNames.KEEPASSXC_MASTER_PASSWORD]: "",
    [EnvNames.KEYCHAIN_ACCOUNT]: app.doShellScript("id -un"),
    [EnvNames.KEYCHAIN_SERVICE]: alfredWorkflowBundleId,
    [EnvNames.SHOW_ATTRIBUTE_VALUES]: "true",
    [EnvNames.SHOW_UNFILLED_ATTRIBUTES]: "false",
    [EnvNames.DESIRED_ATTRIBUTES]: "title,username,password,url,notes",
    [EnvNames.SHOW_PASSWORDS]: "false",
    [EnvNames.ENTRY_DELIMITER]: " › "
}


function isDefaultSettings() {
    return [
        Settings.ALFRED_KEYWORD === DefaultEnvValues[EnvNames.ALFRED_KEYWORD],
        Settings.KEEPASSXC_DB_PATH === DefaultEnvValues[EnvNames.KEEPASSXC_DB_PATH],
        Settings.KEEPASSXC_CLI_PATH === DefaultEnvValues[EnvNames.KEEPASSXC_CLI_PATH],
        Settings.KEEPASSXC_KEYFILE_PATH === DefaultEnvValues[EnvNames.KEEPASSXC_KEYFILE_PATH],
        Settings.KEEPASSXC_MASTER_PASSWORD === DefaultEnvValues[EnvNames.KEEPASSXC_MASTER_PASSWORD],
        Settings.KEYCHAIN_ACCOUNT === DefaultEnvValues[EnvNames.KEYCHAIN_ACCOUNT],
        Settings.KEYCHAIN_SERVICE === DefaultEnvValues[EnvNames.KEYCHAIN_SERVICE],
        Settings.SHOW_ATTRIBUTE_VALUES === DefaultEnvValues[EnvNames.SHOW_ATTRIBUTE_VALUES],
        Settings.SHOW_UNFILLED_ATTRIBUTES === DefaultEnvValues[EnvNames.SHOW_UNFILLED_ATTRIBUTES],
        Settings.DESIRED_ATTRIBUTES === DefaultEnvValues[EnvNames.DESIRED_ATTRIBUTES],
        Settings.SHOW_PASSWORDS === DefaultEnvValues[EnvNames.SHOW_PASSWORDS],
        Settings.ENTRY_DELIMITER === DefaultEnvValues[EnvNames.ENTRY_DELIMITER],
    ].every(Boolean)
}


function isEmptySettings() {
    return [
        Settings.ALFRED_KEYWORD === DefaultEnvValues[EnvNames.ALFRED_KEYWORD],
        Settings.KEEPASSXC_DB_PATH === "",
        Settings.KEEPASSXC_CLI_PATH === "",
        Settings.KEEPASSXC_KEYFILE_PATH === "",
        Settings.KEEPASSXC_MASTER_PASSWORD === "",
        Settings.KEYCHAIN_ACCOUNT === "",
        Settings.KEYCHAIN_SERVICE === "",
        Settings.SHOW_ATTRIBUTE_VALUES === "",
        Settings.SHOW_UNFILLED_ATTRIBUTES === "",
        Settings.DESIRED_ATTRIBUTES === "",
        Settings.SHOW_PASSWORDS === "",
        Settings.ENTRY_DELIMITER === "",
    ].every(Boolean)
}


/**
 * This function resets all environment variables to default values.
 * Also it's necessary to reset Settings object to default values because
 * Settings object takes values from environment and we can't get new
 * environment values in runtime but we need these values.
 */
function resetEnvsToDefaults() {
    for (let env in DefaultEnvValues) {
        let exportable = env === EnvNames.ALFRED_KEYWORD
        setEnv(env, DefaultEnvValues[env], exportable)
    }

    for (let key in Settings) {
        Settings[key] = DefaultEnvValues[EnvNames[key]]
    }
}


function throwCancelErrorIfCancelButton(response) {
    if (response.buttonReturned === cancelButton) {
        throw CancelError
    }
}


function convertYesNoToBool(value) {
    return value === yesButton
}


function showMessage(message) {
    app.displayDialog(message, {
        buttons: ["Ok"],
        defaultButton: "Ok",
        withTitle: windowTitle,
    })
}

function showErrorAndExit(message) {
    showMessage(message)
    throw CancelError
}


function showDialog(message, actionButtons, withCancelButton=true) {
    let buttons = withCancelButton ? [cancelButton].concat(actionButtons): actionButtons
    let response = app.displayDialog(message, {buttons: buttons, withTitle: windowTitle})
    throwCancelErrorIfCancelButton(response)
    return response
}


function askYesOrNo(message, noAsCancel=false) {
    let dialogParameters = {
        buttons: [noButton, yesButton],
        withTitle: windowTitle,
    }

    let response = app.displayDialog(message, dialogParameters)

    if (noAsCancel && response.buttonReturned === noButton) {
        throw CancelError
    }

    return convertYesNoToBool(response.buttonReturned)
}


function askText(message, options={}) {
    let response = app.displayDialog(message, {
        defaultAnswer: options.defaultAnswer || "",
        buttons: [cancelButton, "Continue"],
        withTitle: windowTitle,
        hiddenAnswer: options.hideUserInput || false,
    })

    throwCancelErrorIfCancelButton(response)

    if (options.requireText && !response.textReturned) {
        let errorMessage = "The value cannot be empty.\n\n"
        return askText(errorMessage + message, options)
    }

    return response.textReturned
}


function askFile(message, requiredExtension) {
    let dialogSettings = {
        withPrompt: message,
        multipleSelectionsAllowed: false,
        ofType: [requiredExtension] ? requiredExtension: [],
    }

    if (requiredExtension) {
        dialogSettings["ofType"] = [requiredExtension]
    }

    return app.chooseFile(dialogSettings)
}


function showErrorIfThereIsNoAccountOrService() {
    if (!Settings.KEYCHAIN_ACCOUNT || !Settings.KEYCHAIN_SERVICE) {
        let message = [
            "First configure the keychain account name and the keychain service name. ",
            "This can be changed in the settings."
        ].join("")

        showErrorAndExit(message)
    }
}


function askKeepassXCDBPath() {
    return askFile("Select KeepassXC database file", "dyn.ah62d4rv4ge8003dcta").toString()
}


function askKeepassXCCLIPath() {
    return askFile("Select executable KeepassXC CLI file").toString()
}


function askShowValues() {
    let message = [
        "By default, the workflow shows the attribute values requested from ",
        "KeepassXC, such as password, username, etc. ",
        "You can hide these values and display only the attribute names.",
        "\n\n",
        "Display values?",
    ].join("")

    return askYesOrNo(message)
}


function askShowUnfilledAttributes() {
    let message = [
        "By default, the workflow displays all attributes of records ",
        "requested from KeepassXC. You can hide attributes that have no data. ",
        "For example, if the username field of any record in KeepassXC is ",
        "not filled then it will not be displayed.",
        "\n\n",
        "Display attributes that have no data?",
    ].join("")

    return askYesOrNo(message)
}


function askKeychainData(keychainParameter) {
    let parameterTextName = keychainParameter === EnvNames.KEYCHAIN_ACCOUNT ? "account name" : "service name"
    let settingName = keychainParameter === EnvNames.KEYCHAIN_ACCOUNT ? "KEYCHAIN_ACCOUNT" : "KEYCHAIN_SERVICE"

    let message = [
        "The workflow saves your KeepassXC master password and some ",
        "parameters into the keychain (password management system in macOS). ",
        "These parameters will be used to search for the master password in ",
        `the keychain. The ${parameterTextName} is one of these parameters. `,
        "If there is already a record with a password in the keychain, the ",
        "record will be deleted after changing this parameter.",
        "\n\n",
        "Warning: it is not recommended to change it if you are not sure what it affects.",
        "\n\n",
        `Enter the ${parameterTextName} you want to use.`,
    ].join("")

    let response = askText(message, {defaultAnswer: Settings[settingName], requireText: true})
    let areThereAccountAndService = Settings.KEYCHAIN_ACCOUNT && Settings.KEYCHAIN_SERVICE
    let isNewAccountEntered = response !== Settings[settingName]

    if (areThereAccountAndService && isNewAccountEntered && isTherePasswordInKeychain()) {
        deletePasswordFromKeychain()
        setEnv(EnvNames.KEEPASSXC_MASTER_PASSWORD, "")
    }

    return response
}


function askKeychainAccount() {
    return askKeychainData(EnvNames.KEYCHAIN_ACCOUNT)
}


function askKeychainService() {
    return askKeychainData(EnvNames.KEYCHAIN_SERVICE)
}


/**
 * Adds the password to keychain or updates an keychain item if needed.
 * It's necessary to save the password to environment variable and
 * it will be fetched from a shell command.
 * It should help avoid password leakage.
 */
function addPasswordToKeychain(password, overwrite=false) {
    showErrorIfThereIsNoAccountOrService()

    let account = Settings.KEYCHAIN_ACCOUNT
    let service = Settings.KEYCHAIN_SERVICE
    let temporaryPasswordEnv = "password"
    let command = `security add-generic-password -a ${account} -s ${service}`

    command += ` -w "$${temporaryPasswordEnv}"`

    if (overwrite) {
        command += " -U" // update an entry if it is in keychains
    }

    setTemporaryEnv(temporaryPasswordEnv, password)

    try {
        app.doShellScript(command)
    } catch (err) {
        let passwordExistsErrorNumber = 45

        if (err.errorNumber === passwordExistsErrorNumber) {
            let message = "Your keychain already has an entry with the same service " +
            "name and account name. What do you want to do next?"

            let updateButton = "Update the existing entry"
            let useExistingButton = "Use the existing entry"
            let actionButtons = [updateButton, useExistingButton]
            let response = showDialog(message, actionButtons)

            if (response.buttonReturned === updateButton) {
                overwrite = true
                addPasswordToKeychain(password, overwrite)
            }

        } else if (err.errorNumber > 0) {
            throw err
        }
    } finally {
        unsetTemporaryEnv(temporaryPasswordEnv)
    }
}


function deletePasswordFromKeychain() {
    let account = Settings.KEYCHAIN_ACCOUNT
    let service = Settings.KEYCHAIN_SERVICE

    if (!account || !service) {
        return
    }

    let command = `security delete-generic-password -a ${account} -s ${service}`

    try {
        app.doShellScript(command)
    } catch (err) {
        let passwordDoesNotExistErrorNumber = 44

        if (err.errorNumber === passwordDoesNotExistErrorNumber) {
            // It's considered a successful operation so we ignore it.
        } else if (err.errorNumber > 0) {
            throw err
        }
    }
}


function isTherePasswordInKeychain() {
    showErrorIfThereIsNoAccountOrService()
    let account = Settings.KEYCHAIN_ACCOUNT
    let service = Settings.KEYCHAIN_SERVICE
    let command = `security find-generic-password -a ${account} -s ${service}`

    try {
        app.doShellScript(command)
    } catch (err) {
        let passwordDoesNotExistErrorNumber = 44

        if (err.errorNumber === passwordDoesNotExistErrorNumber) {
            return false
        } else if (err.errorNumber > 0) {
            throw err
        }
    }

    return true
}


function askKeepassXCMasterPassword() {
    showErrorIfThereIsNoAccountOrService()

    if (Settings.KEEPASSXC_MASTER_PASSWORD === maskedPassword) {
        let changePasswordButton = "Change"
        let removePasswordButton = "Remove"
        let actionButtons = [removePasswordButton, changePasswordButton]
        let message = "What would you like to do with your password?"
        let response = showDialog(message, actionButtons)

        if (response.buttonReturned === removePasswordButton) {
            let noAsCancel = true
            let message = [
                "The workflow will forget your password. The next time you ",
                "want to search for KeepassXC records, the workflow will ",
                "ask you to enter your password again.",
                "\n\n",
                "Do you want to continue?",
            ].join("")

            askYesOrNo(message, noAsCancel)
            deletePasswordFromKeychain()
            return ""
        }
    }

    let message = [
        "Enter the master password for your KeepassXC database. If your ",
        "database has no password then leave this field blank and ",
        "press continue.",
    ].join("")

    let userPassword = askText(message, {hideUserInput: true})

    addPasswordToKeychain(userPassword)
    return maskedPassword
}


function askKeepassXCKeyFilePath() {
    if (Settings.KEEPASSXC_KEYFILE_PATH !== "") {
        let removeButton = "Remove"
        let changeButton = "Change"
        let message = "You have the key. You can remove it or define a different one."
        let actionButtons = [removeButton, changeButton]
        let response = showDialog(message, actionButtons)

        if (response.buttonReturned === removeButton) {
            return ""
        }
    }

    return askFile("Select KeepassXC key file").toString()
}


function askDesiredAttributes() {
    let availableAttributes = DefaultEnvValues[EnvNames.DESIRED_ATTRIBUTES].replaceAll(" ", "").split(",")
    let message = [
        "By default, the workflow shows all attributes of requested records ",
        "from KeepassXC: title, username, password, url, notes.",
        "\n\n",
        "Select the attributes you need.",
    ].join("")

    let attributes = app.chooseFromList(availableAttributes, {
        withPrompt: message,
        emptySelectionAllowed: false,
        multipleSelectionsAllowed: true,
        defaultItems: Settings.DESIRED_ATTRIBUTES.replaceAll(" ", "").split(",")
    })

    if (attributes === false) {
        throw CancelError
    }

    return attributes.join(", ")
}


function askShowPassword() {
    let message = [
        "By default, no real passwords are displayed for requested record from KeepassXC. ",
        "They are replaced by special characters.",
        "\n\n",
        "Display real passwords?",
    ].join("")

    return askYesOrNo(message)
}


function askEntryDelimiter() {
    let message = [
        "If a requested record from KeepassXC is in a directory, it will be displayed as follows:",
        "\n\n",
        "directory › record",
        "\n\n",
        "You can change the symbol \"›\" to the one you want.",
    ].join("")
    let currentDelimiter = Settings.ENTRY_DELIMITER
    return askText(message, {defaultAnswer: currentDelimiter, requireText: true})
}


function askAlfredKeyword() {
    let message = [
        "By default \"kp\" is used as the keyword name for this workflow. ",
        "If the keyword name is already in use by another workflow or if you want to ",
        "use a different keyword name then change it here.",
    ].join("")

    return askText(message, {defaultAnswer: Settings.ALFRED_KEYWORD, requireText: true})
}


function setEnv(key, value, exportable=false) {
    let alfredApp = Application('com.runningwithcrayons.Alfred')
    alfredApp.setConfiguration(key, {
        toValue: value,
        inWorkflow: alfredWorkflowBundleId,
        exportable: exportable,
    })
}


function changeSettingKey(argv) {
    let settingKey = argv[0]

    let dialogsMap = {
        [EnvNames.ALFRED_KEYWORD]: askAlfredKeyword,
        [EnvNames.KEEPASSXC_DB_PATH]: askKeepassXCDBPath,
        [EnvNames.KEEPASSXC_CLI_PATH]: askKeepassXCCLIPath,
        [EnvNames.KEEPASSXC_KEYFILE_PATH]: askKeepassXCKeyFilePath,
        [EnvNames.KEYCHAIN_ACCOUNT]: askKeychainAccount,
        [EnvNames.KEYCHAIN_SERVICE]: askKeychainService,
        [EnvNames.SHOW_ATTRIBUTE_VALUES]: askShowValues,
        [EnvNames.SHOW_UNFILLED_ATTRIBUTES]: askShowUnfilledAttributes,
        [EnvNames.DESIRED_ATTRIBUTES]: askDesiredAttributes,
        [EnvNames.KEEPASSXC_MASTER_PASSWORD]: askKeepassXCMasterPassword,
        [EnvNames.SHOW_PASSWORDS]: askShowPassword,
        [EnvNames.ENTRY_DELIMITER]: askEntryDelimiter,
    }

    let response = dialogsMap[settingKey]()
    let exportable = settingKey === EnvNames.ALFRED_KEYWORD

    setEnv(settingKey, response, exportable)
    showMessage("The settings was changed successfully.")
}


function showResetDialog() {
    let message = "This action resets all your current settings to default values. Do you want to continue?"
    let noAsCancel = true
    askYesOrNo(message, noAsCancel)
}


function resetSettings() {
    showResetDialog()
    deletePasswordFromKeychain()
    resetEnvsToDefaults()
    showMessage("The settings were reset to defaults successfully.")
}


function init() {
    if (!isEmptySettings() && !isDefaultSettings()) {
        showResetDialog()
    }

    deletePasswordFromKeychain()
    resetEnvsToDefaults()

    let db = askKeepassXCDBPath()

    let keyfile = askYesOrNo("Do you have a key file") ?
        askKeepassXCKeyFilePath() :
        DefaultEnvValues[EnvNames.KEEPASSXC_KEYFILE_PATH]

    let password = askKeepassXCMasterPassword()

    setEnv(EnvNames.KEEPASSXC_DB_PATH, db)
    setEnv(EnvNames.KEEPASSXC_KEYFILE_PATH, keyfile)
    setEnv(EnvNames.KEEPASSXC_MASTER_PASSWORD, password)
    showMessage("The initialization was successful.")
}


function getActionFuncByName(actionName) {
    let actionFuncsMap = {
        change: changeSettingKey,
        reset: resetSettings,
        init: init,
    }

    return actionFuncsMap[actionName]
}


function run(argv) {
    try {
        let actionName = argv[0]
        let actionFunc = getActionFuncByName(actionName)
        actionFunc(argv.slice(1))
    } catch (err) {
        if (err.errorNumber !== cancelErrorNumber) {
            showMessage("An error has occurred.\n\n" + err.message)
        }
    }
}