const registerValidator = (elementId, validator) => {
    document.getElementById(elementId).onchange = validator;
    document.getElementById(elementId).oninput = validator;
}

const errorMessageForId = (elementId) => {
    if (document && document.getElementById(elementId)) {
        return document.getElementById(elementId).validationMessage;
    }
    return '';
}

const validatePath = (elementId) => {
    let e = document.getElementById(elementId);
    if (e.value.length > 0 && e.value[0] !== '/') {
        e.setCustomValidity("Path must start with '/'!")
    } else if (e.value.length == 0) {
        e.setCustomValidity("Path cannot be empty!")
    } else {
        e.setCustomValidity("");
    }
};

const isValidProtectedElement = (e) => {
    const ipv4Pattern = /^(\d{1,3}\.){3}\d{1,3}$/;
    const ipv6Pattern = /^([a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$/;
    const ipv4RangePattern = /^(\d{1,3}\.){3}\d{1,3}\/\d{1,2}$/;
    const ipv6RangePattern = /^([a-fA-F0-9]{1,4}:){1,7}[a-fA-F0-9]{0,4}\/\d{1,3}$/;

    if (ipv4Pattern.test(e)) {
        return e.split('.').every(num => parseInt(num, 10) >= 0 && parseInt(num, 10) <= 255);
    }

    if (ipv6Pattern.test(e)) {
        return true;
    }

    if (ipv4RangePattern.test(e)) {
        const [address, prefix] = e.split('/');
        return isValidProtectedElement(address) && parseInt(prefix, 10) >= 0 && parseInt(prefix, 10) <= 32;
    }

    if (ipv6RangePattern.test(e)) {
        const [address, prefix] = e.split('/');
        return isValidProtectedElement(address) && parseInt(prefix, 10) >= 0 && parseInt(prefix, 10) <= 128;
    }

    return false;
}

const validateProtectedRanges = (elementId) => {
    let e = document.getElementById(elementId);
    const lines = e.value.split(/\r?\n/);
    for (let idx = 0; idx < lines.length; ++idx) {
        if (lines[idx].length > 0 && !isValidProtectedElement(lines[idx])) {
            e.setCustomValidity("Incorrect format of IP ranges!");
            return;
        }
    }
    e.setCustomValidity("");
}

export { registerValidator, errorMessageForId, validatePath, validateProtectedRanges };
