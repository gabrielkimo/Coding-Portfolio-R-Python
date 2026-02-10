library(bsplus)
library(plotly)
library(tidyverse)

ui <- fluidPage(
  titlePanel("Advanced Interactive Data Explorer with Plotly Hover Tooltips"),
  
  sidebarLayout(
    sidebarPanel(
      selectInput("variable", "Select Variable:", choices = names(mtcars)) %>%
        bs_embed_tooltip(title = "Choose a variable from the dataset."),
      
      selectInput("plotType", "Select Plot Type:", 
                  choices = c("Scatter Plot", "Histogram", "Box Plot")) %>%
        bs_embed_tooltip(title = "Choose the type of plot to display."),
      
      sliderInput("mpgRange", "Filter by MPG range:", 
                  min = min(mtcars$mpg), max = max(mtcars$mpg), 
                  value = range(mtcars$mpg), step = 1) %>%
        bs_embed_tooltip(title = "Adjust to filter data by miles per gallon (MPG)."),
      
      checkboxInput("showTrend", "Show trend line in scatter plot", FALSE) %>%
        bs_embed_tooltip(title = "Check to add a trend line to scatter plots."),
      
      checkboxInput("showGrid", "Show grid lines", TRUE) %>%
        bs_embed_tooltip(title = "Toggle grid lines on the plot.")
    ),
    
    mainPanel(
      plotlyOutput("plot"),  # Using plotlyOutput for interactive plot
      verbatimTextOutput("summary")
    )
  )
)

server <- function(input, output) {
  filtered_data <- reactive({
    # Filter mtcars based on the MPG slider input
    data <- mtcars %>% filter(mpg >= input$mpgRange[1] & mpg <= input$mpgRange[2])
    
    # Notify if no data is available
    if (nrow(data) == 0) {
      showNotification("No data available in the selected MPG range", type = "error")
    }
    
    data
  })
  
  output$plot <- renderPlotly({
    data <- filtered_data()
    
    # Check if there's data to plot
    if (nrow(data) == 0) return(NULL)
    
    # Check if the selected variable is numeric when Scatter Plot is chosen
    if (input$plotType == "Scatter Plot" && !is.numeric(data[[input$variable]])) {
      showNotification("Please select a numeric variable for the scatter plot.", type = "error")
      return(NULL)
    }
    
    # Base ggplot
    p <- ggplot(data, aes_string(x = input$variable, y = "mpg")) +
      labs(x = input$variable, y = "MPG", 
           title = paste(input$plotType, "of", input$variable, "vs MPG")) +
      theme_minimal()
    
    # Add selected plot type
    if (input$plotType == "Scatter Plot") {
      p <- p + geom_point(aes(text = paste(input$variable, "=", round(data[[input$variable]], 2),
                                           "<br>MPG =", round(data$mpg, 2))))
      
      # Add trend line if selected
      if (input$showTrend) {
        p <- p + geom_smooth(method = "lm", se = FALSE, color = "blue")
      }
      
    } else if (input$plotType == "Histogram") {
      p <- ggplot(data, aes_string(x = input$variable)) +
        geom_histogram(fill = "lightblue", color = "black") +
        labs(y = "Frequency", title = paste("Histogram of", input$variable))
      
    } else if (input$plotType == "Box Plot") {
      p <- ggplot(data, aes_string(x = "factor(1)", y = input$variable)) +
        geom_boxplot() +
        labs(x = "", y = input$variable, title = paste("Box Plot of", input$variable))
    }
    
    # Toggle grid lines
    if (!input$showGrid) {
      p <- p + theme(panel.grid = element_blank())
    }
    
    # Convert ggplot to plotly for hover tooltips
    ggplotly(p, tooltip = "text")
  })
  
  output$summary <- renderPrint({
    # Ensure that variable selected for summary is present and valid
    if (!is.null(filtered_data()[[input$variable]])) {
      summary(filtered_data()[[input$variable]])
    } else {
      "Summary not available for selected variable."
    }
  })
}

shinyApp(ui = ui, server = server)

