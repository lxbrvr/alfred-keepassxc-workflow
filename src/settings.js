ObjC.import("stdlib")


let app = Application.currentApplication()
app.includeStandardAdditions = true

const windowTitle = "Alfred KeepassXC"
const maskedPassword = "••••••••"
const alfredWorkflowBundleId = $.getenv("alfred_workflow_bundleid")
const cancelButton = "Cancel"

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
    return value === "Yes"
}


function showMessage(message) {
    app.displayDialog(message, {
        buttons: ["Ok"],
        defaultButton: "Ok",
        withTitle: windowTitle,
    })
}


function showDialog(message, actionButtons, withCancelButton=true) {
    let buttons = withCancelButton ? [cancelButton].concat(actionButtons): actionButtons
    let response = app.displayDialog(message, {buttons: buttons, withTitle: windowTitle})
    throwCancelErrorIfCancelButton(response)
    return response
}


function askYesOrNo(message, noAsCancel=false) {
    let dialogParameters = {
        buttons: ["No", "Yes"],
        withTitle: windowTitle,
    }

    let response = app.displayDialog(message, dialogParameters)

    if (noAsCancel && response.buttonReturned === "No") {
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


function askKeepassXCDBPath() {
    return askFile("Select KeepassXC database file", "dyn.ah62d4rv4ge8003dcta").toString()
}


function askKeepassXCCLIPath() {
    return askFile("Select executable KeepassXC CLI file").toString()
}


function askShowValues() {
    return askYesOrNo("Show values for attributes?")
}


function askShowUnfilledAttributes() {
    return askYesOrNo("Show unfilled attributes?")
}


function askKeychainAccount() {
    let defaultAnswer = Settings.KEYCHAIN_ACCOUNT
    let message = "Enter the account name you want to use for the keychain."
    return askText(message, {defaultAnswer: defaultAnswer, requireText: true})
}


function askKeychainService() {
    let currentService = Settings.KEYCHAIN_SERVICE
    let message = "Enter the service name you want to use for the keychain."
    return askText(message, {defaultAnswer: currentService, requireText: true})
}


/**
 * Adds the password to keychain or updates an keychain item if needed.
 * It's necessary to save the password to environment variable and
 * it will be fetched from a shell command.
 * It should help avoid password leakage.
 */
function addPasswordToKeychain(password, overwrite=false) {
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


function askKeepassXCMasterPassword() {
    if (Settings.KEEPASSXC_MASTER_PASSWORD === maskedPassword) {
        let changePasswordButton = "Change"
        let removePasswordButton = "Remove"
        let actionButtons = [removePasswordButton, changePasswordButton]
        let message = "What would you like to do with your password?"
        let response = showDialog(message, actionButtons)

        if (response.buttonReturned === removePasswordButton) {
            let noAsCancel = true
            let message = "The workflow will forget your password. Do you want to continue?"
            askYesOrNo(message, noAsCancel)
            deletePasswordFromKeychain()
            return ""
        }
    }

    let message = "Enter the password to use KeepassXC database.\nif you don't have the password then press continue."
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
    let attributes = app.chooseFromList(availableAttributes, {
        withPrompt: "Select the attributes you need",
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
    return askYesOrNo("Show entry passwords in Alfred?")
}


function askEntryDelimiter() {
    let message = "Enter the delimiter for entries path."
    let currentDelimiter = Settings.ENTRY_DELIMITER
    return askText(message, {defaultAnswer: currentDelimiter, requireText: true})
}


function askAlfredKeyword() {
    let message = "Enter the keyword name for using it in Alfred."
    let currentKeyword = Settings.ALFRED_KEYWORD
    return askText(message, {defaultAnswer: currentKeyword, requireText: true})
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