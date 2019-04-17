// 6 Tests
import io.github.bonigarcia.wdm.WebDriverManager;
import junit.framework.TestCase;
import org.junit.After;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;

import java.util.List;
import java.util.concurrent.TimeUnit;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertSame;
import static org.junit.Assert.assertTrue;

public class ResultsPageTesting {
    private WebDriver driver;

    @BeforeClass
    public static void setupClass() {
        WebDriverManager.chromedriver().setup();
    }

    @Before
    public void setupTest() {
        driver = new ChromeDriver();
        driver.get("http://bookbrain.club");

        WebElement searchBar = driver.findElement(By.id("autocomplete"));
        WebElement searchButton = driver.findElement(By.id("submit"));
        //type in T
        searchBar.sendKeys("T");
        searchButton.click();
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);
    }

    @After
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    public void resultsDisplayedIsAtMost10() {
        WebElement bookResults = driver.findElement(By.cssSelector("div.list-group"));
        List<WebElement> bookResultsDisplayed = bookResults.findElements(By.tagName("a.list-group-item list-group-item-action"));
        assertTrue(bookResultsDisplayed.size() <= 10);
    }

    @Test
    public void resultIsClickable() {
        WebElement bookResults = driver.findElement(By.cssSelector("div.list-group"));
        bookResults.findElement(By.cssSelector("a.list-group-item.list-group-item-action")).click();

        String currentURL = driver.getCurrentUrl();
        assertEquals("http://bookbrain.club/book/20", currentURL);
    }

    @Test
    public void paginatorDefaultisPage1() {
        WebElement currentPage = driver.findElement(By.cssSelector("li#current.page-item.active"));
        String number = currentPage.getText().toString();
        assertTrue(number.equals("1"));
    }

    @Test
    public void paginatorClickingPage2Works() {
        WebElement paginator = driver.findElement(By.cssSelector("ul.pagination.justify-content-center"));
        WebElement page2Button = paginator.findElements(By.tagName("li")).get(2);

        //make sure button I am clicking is the page 2 button
        assertEquals("2", page2Button.findElement(By.tagName("a")).getText().toString());
        page2Button.click();
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement currentPage = driver.findElement(By.cssSelector("li#current.page-item.active"));
        String number = currentPage.getText().toString();
        assertTrue(number.equals("2"));
    }

    @Test
    public void paginatorClickingLastPageWorks() {
        WebElement paginator = driver.findElement(By.cssSelector("ul.pagination.justify-content-center"));
        WebElement lastPageButton = paginator.findElements(By.tagName("li")).get(4);

        //make sure button I am clicking is the >> button
        assertEquals("»", lastPageButton.findElement(By.tagName("a")).getText().toString());
        lastPageButton.click();
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        paginator = driver.findElement(By.cssSelector("ul.pagination.justify-content-center"));
        String pageItShouldBe = paginator.findElements(By.tagName("li")).get(3).getText().toString();
        String currentPage = driver.findElement(By.cssSelector("li#current.page-item.active")).getText().toString();

        assertEquals(pageItShouldBe, currentPage);
    }

    @Test
    public void paginatorClickingFirstPageWorks() {
        WebElement paginator = driver.findElement(By.cssSelector("ul.pagination.justify-content-center"));
        WebElement lastPageButton = paginator.findElements(By.tagName("li")).get(0);

        //make sure button I am clicking is the << button
        assertEquals("«", lastPageButton.findElement(By.tagName("a")).getText().toString());
        lastPageButton.click();
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        paginator = driver.findElement(By.cssSelector("ul.pagination.justify-content-center"));
        String pageItShouldBe = paginator.findElements(By.tagName("li")).get(1).getText().toString();
        String currentPage = driver.findElement(By.cssSelector("li#current.page-item.active")).getText().toString();

        assertEquals(pageItShouldBe, currentPage);
    }


}
