# Ghidra plugin that asks Groq API to explain functions
# @author fbader927
# @category API
# @keybinding Ctrl-Alt-G
# @menupath Tools.GroqGhidra
# @toolbar

import urllib2
import json
from ghidra.util.task import TaskMonitor
from ghidra.app.decompiler import DecompInterface

# Groq API key (get it here for free https://groq.com/)
GROQ_API_KEY = 'groq API key here'


def explainFunction(c_code):
    """
        Calls the Groq API to explain the given code.

        Args:
            c_code (str): The code to be explained.

        Returns:
            str: The explanation provided by the API.
    """
    url = 'https://api.groq.com/openai/v1/chat/completions'
    data = {
        "messages": [
            {"role": "user", "content": "You are analyzing a decompiled function from Ghidra. Attempt to find patterns within the code to help decompile the program, possibly offering steps on what to investigate next:\n" + c_code}
        ],
        "model": "llama3-70b-8192"
    }
    data = json.dumps(data)

    req = urllib2.Request(url, data.encode('utf-8'),
                          {
                              'Authorization': 'Bearer ' + GROQ_API_KEY,
                              'Content-Type': 'application/json',
                              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    })

    try:
        response = urllib2.urlopen(req)
        response_data = json.loads(response.read())
        if "error" in response_data:
            raise ValueError(response_data["error"])
        return response_data["choices"][0]["message"]["content"]
    except urllib2.HTTPError as e:
        print("HTTP Error:", e.code, e.reason)
        print("Response body:", e.read())
        raise
    except urllib2.URLError as e:
        print("URL Error:", e.reason)
        raise
    except ValueError as e:
        print("Value Error:", str(e))
        raise
    except Exception as e:
        print("Unexpected Error:", str(e))
        raise


def getCurrentDecompiledFunction():
    """
        Returns the C code for the function currently selected in the Ghidra decompiler.

        Returns:
            str: The C code for the selected function.
    """
    # Reference: https://ghidra.re/ghidra_docs/api/ghidra/app/decompiler/DecompInterface.html

    monitor = TaskMonitor.DUMMY
    decompiler = DecompInterface()
    decompiler.openProgram(currentProgram)
    currentAddress = currentLocation.getAddress()
    function = getFunctionContaining(currentAddress)

    if function is None:
        raise ValueError("No function is currently selected.")
    try:
        return decompiler.decompileFunction(function, 30, monitor).getDecompiledFunction().getC()
    except Exception as e:
        raise ValueError("Unable to decompile function: " + str(e))


try:
    c_code = getCurrentDecompiledFunction()
    print("Decompiled Code:\n", c_code)
    explanation = explainFunction(c_code)
    print(explanation)
except ValueError as e:
    print(e)
except Exception as e:
    print("An error occurred:", str(e))
