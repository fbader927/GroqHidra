# GroqHidra
A Ghidra plugin that uses the Groq API for Llama3 70b to explain functions. A free alternative to OpenAI's API. 


![image](https://github.com/fbader927/GroqHidra/assets/50185837/b42c34ba-59ac-4fd5-af74-9a3707cb09a4)



Steps to install:
1. Download GroqHidra.py
2. Open Script Manager in Ghidra
3. Click 'New' and add new script, select 'Python' as language and name it GroqHidra.py
4. Copy and paste the code from GroqHidra.py into the editor
5. Enter your Groq API key into the code

Save the script, then execute an analysis on any decompiled function by pressing 'CTRL' + 'ALT' + 'G'. The analysis will be displayed in the console after it's loaded. 
