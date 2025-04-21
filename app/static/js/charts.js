// Make sure Chart.js is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Function to format currency
    function formatCurrency(value) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 2
        }).format(value);
    }
    
    // Budget Chart Setup - If element exists
    const budgetChartEl = document.getElementById('budgetChart');
    if (budgetChartEl) {
        const ctx = budgetChartEl.getContext('2d');
        
        // Chart data will be populated by the template
        // See the budget.html template for implementation
    }
    
    // Expense Category Chart - If element exists
    const expenseCategoryChartEl = document.getElementById('expenseCategoryChart');
    if (expenseCategoryChartEl) {
        const ctx = expenseCategoryChartEl.getContext('2d');
        const categoryData = JSON.parse(expenseCategoryChartEl.dataset.categories || '[]');
        
        if (categoryData.length > 0) {
            const labels = categoryData.map(item => item.category);
            const data = categoryData.map(item => item.amount);
            
            // Generate random colors for each category
            const backgroundColors = labels.map(() => 
                `rgba(${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, ${Math.floor(Math.random() * 255)}, 0.5)`
            );
            
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Expenses by Category',
                        data: data,
                        backgroundColor: backgroundColors,
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.label || '';
                                    const value = context.raw || 0;
                                    const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                    const percentage = Math.round((value / total) * 100);
                                    return `${label}: ${formatCurrency(value)} (${percentage}%)`;
                                }
                            }
                        }
                    }
                }
            });
        }
    }
    
    // Monthly Expense Trend Chart - If element exists
    const monthlyTrendChartEl = document.getElementById('monthlyTrendChart');
    if (monthlyTrendChartEl) {
        const ctx = monthlyTrendChartEl.getContext('2d');
        const monthlyData = JSON.parse(monthlyTrendChartEl.dataset.monthly || '[]');
        
        if (monthlyData.length > 0) {
            const labels = monthlyData.map(item => item.month);
            const expenses = monthlyData.map(item => item.expenses);
            const budgets = monthlyData.map(item => item.budget);
            
            new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [
                        {
                            label: 'Expenses',
                            data: expenses,
                            borderColor: 'rgba(255, 99, 132, 1)',
                            backgroundColor: 'rgba(255, 99, 132, 0.2)',
                            fill: true,
                            tension: 0.1
                        },
                        {
                            label: 'Budget',
                            data: budgets,
                            borderColor: 'rgba(54, 162, 235, 1)',
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            fill: true,
                            tension: 0.1
                        }
                    ]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true,
                            title: {
                                display: true,
                                text: 'Amount ($)'
                            },
                            ticks: {
                                callback: function(value) {
                                    return '$' + value;
                                }
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    const label = context.dataset.label || '';
                                    const value = context.raw || 0;
                                    return `${label}: ${formatCurrency(value)}`;
                                }
                            }
                        }
                    }
                }
            });
        }
    }
});