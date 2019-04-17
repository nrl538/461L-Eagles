// 5 TESTS
import io.github.bonigarcia.wdm.WebDriverManager;
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

import static junit.framework.TestCase.assertEquals;

public class AboutPageTesting {
    private WebDriver driver;
    private List<WebElement> phasesAndDocumentation;

    @BeforeClass
    public static void setupClass() {
        WebDriverManager.chromedriver().setup();
    }

    @Before
    public void setupTest() {
        driver = new ChromeDriver();
        driver.get("http://bookbrain.club/about");
        driver.manage().timeouts().implicitlyWait(3, TimeUnit.SECONDS);

        WebElement sourcesToolsAndGitHub = driver.findElement(By.id("about-us-sources"));
        WebElement sources = sourcesToolsAndGitHub.findElement(By.cssSelector("ul.list-group"));
        phasesAndDocumentation = sources.findElements(By.tagName("li"));
    }

    @After
    public void teardown() {
        if (driver != null) {
            driver.quit();
        }
    }

    @Test
    public void goodReadsLinkWorks() {
        WebElement goodReadsLink = phasesAndDocumentation.get(0).findElement(By.tagName("a"));

        assertEquals("Goodreads", goodReadsLink.getText().toString());

        goodReadsLink.click();

        String currentURL = driver.getCurrentUrl();
        assertEquals("https://www.goodreads.com/", currentURL);
    }

    @Test
    public void barnesAndNoblesLinkWorks() {
        WebElement barnesAndNoblesLink = phasesAndDocumentation.get(1).findElements(By.tagName("a")).get(0);

        assertEquals("Barnes & Nobles", barnesAndNoblesLink.getText().toString());

        barnesAndNoblesLink.click();

        String currentURL = driver.getCurrentUrl();
        assertEquals("https://www.barnesandnoble.com/", currentURL);
    }

    @Test
    public void goodReadsSecondLinkWorks() {
        WebElement goodReads2Link = phasesAndDocumentation.get(1).findElements(By.tagName("a")).get(1);

        assertEquals("Goodreads", goodReads2Link.getText().toString());

        goodReads2Link.click();

        String currentURL = driver.getCurrentUrl();
        assertEquals("https://www.goodreads.com/", currentURL);
    }

    @Test
    public void iDreamBooksWorks() {
        WebElement iDreamBooksLink = phasesAndDocumentation.get(1).findElements(By.tagName("a")).get(2);

        assertEquals("IDreamBooks", iDreamBooksLink.getText().toString());

        iDreamBooksLink.click();

        String currentURL = driver.getCurrentUrl();
        assertEquals("https://idreambooks.com/", currentURL);
    }

    @Test
    public void githubWorks() {
        WebElement githubLink = phasesAndDocumentation.get(2).findElement(By.tagName("a"));

        assertEquals("team Github.", githubLink.getText().toString());

        githubLink.click();

        String currentURL = driver.getCurrentUrl();
        assertEquals("https://github.com/Flandini/461L-Eagles/tree/master/scraping", currentURL);
    }
}