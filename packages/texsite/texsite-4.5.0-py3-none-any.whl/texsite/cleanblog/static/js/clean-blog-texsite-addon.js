const copyButtonLabel = 'Copy'
const copiedButtonLabel = 'Copied!'

function prepareCodeCopyButtons() {
  const blocks = document.querySelectorAll('*.cbta-code-container')

  blocks.forEach((block) => {
    const button = block.querySelector('button')

    button.innerText = copyButtonLabel
    button.addEventListener('click', async () => {
      await copyCode(block)
    })
  })
}

async function copyCode(block) {
  let code = block.querySelector('code')
  let button = block.querySelector('button')
  let text = code.innerText

  await navigator.clipboard.writeText(text)
  button.innerText = copiedButtonLabel
  setTimeout(()=> {
    button.innerText = copyButtonLabel
  }, 700)
}
