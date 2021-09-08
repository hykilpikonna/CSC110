// This is to complete ucheck.utoronto.ca

// Load JQuery
function loadJS(url)
{
    const head = document.getElementsByTagName('head')[0];
    const script = document.createElement('script');
    script.type = 'text/javascript';
    script.src = url;
    script.onload = () => console.log(`${url} loaded.`)
    head.appendChild(script);
}
loadJS('https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js')

// Report no symptoms on the report symptoms page
function report()
{
    // Repeat
    let task = setInterval(() =>
    {
        // Check if it's done
        let submit = $('span:contains(Submit)')
        if (!submit.parent()[0].classList.contains('Mui-disabled'))
        {
            console.log('Done, clicking submit')
            clearInterval(task)
            submit.click()
        }

        // Click no buttons
        // Old method: select by class (doesn't work because class names are randomized.
        // Array.from(document.querySelectorAll('.sc-qbELi.eWIawQ')).filter(it => it.querySelector('span').innerHTML === 'No').forEach(it => it.click())
        // New method: select by content and filter by color (white means unselected)
        $('span:contains(No)').parent().filter((i, it) => $(it).css('background-color') === 'rgb(255, 255, 255)').click()

        // Scroll to bottom
        window.scrollTo(0, document.body.scrollHeight);

    }, 100)
}
report()


