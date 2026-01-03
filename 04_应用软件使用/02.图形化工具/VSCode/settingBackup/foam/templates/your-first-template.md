# Foam Note Templates

Foam includes note templates!

This allows you to easily create notes that have similar structure without having to use copy/paste :)

Templates support the [VS Code's Snippet Syntax](https://code.visualstudio.com/docs/editor/userdefinedsnippets#_snippet-syntax), which means you can:

- add variables to the newly created note
- add tabstop to automatically navigate to the key parts of the note, just like a form
Below you can see an example showing a todo list and a timestamp.

## Todo List

1. ${1:First tabstop}
2. ${2:A second tabstop}
3. ${3:A third tabstop}

Note Created: ${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}

---

Try out the above example by running the `Foam: Create New Note From Template` command and selecting the `your-first-template` template. Notice what happens when your new note is created!

To remove this template, simply delete the `.foam/templates/your-first-template.md` file.

Enjoy!

# Foam 笔记模板

Foam 包含笔记模板功能！

这使您能够轻松创建结构相似的笔记，无需再使用复制/粘贴的方式 :)

模板支持 [VS Code 的代码片段语法](https://code.visualstudio.com/docs/editor/userdefinedsnippets#_snippet-syntax)，这意味着您可以：

- 为新创建的笔记添加变量
- 添加跳转停靠点，以便自动导航到笔记的关键部分，就像填写表单一样

下方您可以看到一个示例，展示了待办事项列表和时间戳。

## 待办事项列表

1.  ${1:第一个跳转停靠点}
2.  ${2:第二个跳转停靠点}
3.  ${3:第三个跳转停靠点}

笔记创建于：${CURRENT_YEAR}-${CURRENT_MONTH}-${CURRENT_DATE}

---

您可以通过运行 `Foam: 从模板创建新笔记` 命令并选择 `your-first-template` 模板来尝试上面的示例。注意观察新笔记创建时会发生什么！

要删除此模板，只需删除 `.foam/templates/your-first-template.md` 文件即可。

希望您喜欢这个功能！