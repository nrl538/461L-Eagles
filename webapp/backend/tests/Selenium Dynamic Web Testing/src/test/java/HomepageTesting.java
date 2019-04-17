// 13 Tests

import io.github.bonigarcia.wdm.WebDriverManager;
import org.junit.*;
import org.openqa.selenium.*;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.support.ui.Select;

import java.util.List;
import java.util.NoSuchElementException;
import java.util.concurrent.TimeUnit;

import static org.junit.Assert.*;


public class HomepageTesting {
    private WebDriver driver;

    @BeforeClass
    public static void setupClass() {
        WebDriverManager.chromedriver().setup();
    }

    @Before
    public void setupTest() {
        driver = new ChromeDriver();
        driver.get("http://bookbrain.club");
    }

    @After
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    public void aboutLinkWorks() {
        driver.findElement(By.linkText("About")).click();
        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/about", currentURL);
    }

    @Test
    public void homeLinkWorks() {
        driver.findElement(By.cssSelector("a.nav-link")).click();
        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/", currentURL);
    }

    @Test
    public void searchButtonWorks() {
        driver.get("http://bookbrain.club");
        driver.findElement(By.cssSelector("button.btn.btn-outline-secondary")).click();
        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/search/", currentURL);
    }

    @Test
    public void registerButtonWorks() {
        driver.findElement(By.cssSelector("a.btn.my-2.my-sm-0")).click();
        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/register", currentURL);
    }

    @Test
    public void loginButtonWorks() {
        driver.findElement(By.id("login")).click();
        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/login", currentURL);
    }

    @Test
    public void logoutButtonWorks() {
        driver.findElement(By.id("login")).click();
        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/login", currentURL);
    }

    @Test
    public void logoLinkWorks() {
        driver.get("http://bookbrain.club");
        driver.findElement(By.cssSelector("a.navbar-brand")).click();
        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/", currentURL);
    }

    @Test
    public void searchByWorks() {
        WebElement searchOptions = driver.findElement(By.id("searchOptions"));
        Select searchSelect = new Select(searchOptions);

        assertEquals("Search by...", searchSelect.getFirstSelectedOption().getText().toString());

        searchSelect.selectByVisibleText("Title");
        assertEquals("Title", searchSelect.getFirstSelectedOption().getText().toString());

        searchSelect.selectByVisibleText("Author");
        assertEquals("Author", searchSelect.getFirstSelectedOption().getText().toString());

        searchSelect.selectByVisibleText("ISBN");
        assertEquals("ISBN", searchSelect.getFirstSelectedOption().getText().toString());

        searchSelect.selectByVisibleText("Search by...");
        assertEquals("Search by...", searchSelect.getFirstSelectedOption().getText().toString());
    }

    @Test
    public void autocompleteForSearchByIsSizeAtMost10() {
        WebElement searchBar = driver.findElement(By.id("autocomplete"));
        //type in T
        searchBar.sendKeys("T");
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement suggestions = driver.findElement(By.id("ui-id-1"));
        List<WebElement> suggestionsDisplayed = suggestions.findElements(By.tagName("li"));
        assertTrue(suggestionsDisplayed.size() <= 10);
    }

    @Test
    public void autocompleteForTitleIsSizeAtMost10() {
        WebElement searchBar = driver.findElement(By.id("autocomplete"));

        WebElement searchOptions = driver.findElement(By.id("searchOptions"));

        Select searchSelect = new Select(searchOptions);
        searchSelect.selectByVisibleText("Title");

        //type in T
        searchBar.sendKeys("T");
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement suggestions = driver.findElement(By.id("ui-id-1"));
        List<WebElement> suggestionsDisplayed = suggestions.findElements(By.tagName("li"));
        assertTrue(suggestionsDisplayed.size() <= 10);
    }

    @Test
    public void autocompleteForAuthorIsSizeAtMost10() {
        WebElement searchBar = driver.findElement(By.id("autocomplete"));

        WebElement searchOptions = driver.findElement(By.id("searchOptions"));

        Select searchSelect = new Select(searchOptions);
        searchSelect.selectByVisibleText("Author");

        //type in T
        searchBar.sendKeys("T");
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement suggestions = driver.findElement(By.id("ui-id-1"));
        List<WebElement> suggestionsDisplayed = suggestions.findElements(By.tagName("li"));
        assertTrue(suggestionsDisplayed.size() <= 10);
    }

    @Test
    public void autocompleteForISBNIsSizeAtMost10() {
        WebElement searchBar = driver.findElement(By.id("autocomplete"));

        WebElement searchOptions = driver.findElement(By.id("searchOptions"));

        Select searchSelect = new Select(searchOptions);
        searchSelect.selectByVisibleText("ISBN");

        //type in T
        searchBar.sendKeys("1");
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement suggestions = driver.findElement(By.id("ui-id-1"));
        List<WebElement> suggestionsDisplayed = suggestions.findElements(By.tagName("li"));
        assertTrue(suggestionsDisplayed.size() <= 10);
    }

    @Test
    public void autocompleteForISBNIsOnlyNumbers() {
        WebElement searchBar = driver.findElement(By.id("autocomplete"));

        WebElement searchOptions = driver.findElement(By.id("searchOptions"));

        Select searchSelect = new Select(searchOptions);
        searchSelect.selectByVisibleText("ISBN");

        //type in T
        int randomNumber = ( (int)(Math.random( )*10) +1);
        searchBar.sendKeys(Integer.toString(randomNumber));
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement suggestions = driver.findElement(By.id("ui-id-1"));
        List<WebElement> suggestionsDisplayed = suggestions.findElements(By.tagName("li"));

        //make sure that every suggestion is only comprised of numbers
        for (WebElement suggestion: suggestionsDisplayed) {
            for (Character c: suggestion.getText().toString().toCharArray()) {
                assertTrue(Character.isDigit(c));
            }
        }
    }


    public WebElement searchButton() {
        return driver.findElement(By.cssSelector(""));
    }
}
