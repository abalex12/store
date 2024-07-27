$(document).ready(function() {
    let currentCategoryName = '';
    let totalPurchasePrice = 0;
    let totalSalePrice = 0;

    $('#categoryList').on('click', 'a', function(e) {
        e.preventDefault();
        const categoryId = $(this).data('category-id');
        currentCategoryName = $(this).text().trim().split('\n')[0];

        $('#categoryList a').removeClass('active');
        $(this).addClass('active');
        
        loadBrandsAndProducts(categoryId);
    });

    function loadBrandsAndProducts(categoryId) {
        $.get(inventoryUrl, { action: 'get_brands', category_id: categoryId }, function(brands) {
            let productHtml = `
                <div class="card shadow-sm mb-4">
                    <div class="card-header bg-primary text-white">
                        <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                           <h5 class="mb-0">${currentCategoryName} Products</h5>
                           <a href="/export-products/?category_id=${categoryId}" class="btn btn-light btn-sm">Export to Excel</a>
                        </div>
                    </div>
                    <div class="card-body p-0">
                        <div class="table-responsive">
                            <table class="table table-hover table-striped mb-0">
                                <thead class="table-light">
                                    <tr>
                                        <th class="text-center">Brand</th>
                                        <th class="text-center">Brand Logo</th>
                                        <th class="text-center">Product Image</th>
                                        <th class="text-center">Product</th>
                                        <th class="text-center">Stock</th>
                                        <th class="text-center">Purchase Price</th>
                                        <th class="text-center">Sale Price</th>
                                    </tr>
                                </thead>
                                <tbody id="productTableBody">
                                </tbody>
                                <tfoot id="categoryTotalRow">
                                </tfoot>
                            </table>
                        </div>
                    </div>
                </div>`;
            $('#productList').html(productHtml);

            totalPurchasePrice = 0;
            totalSalePrice = 0;

            let brandsProcessed = 0;
            brands.forEach(function(brand, index) {
                loadProductsForBrand(brand, index, function(brandTotals) {
                    totalPurchasePrice += brandTotals.purchasePrice;
                    totalSalePrice += brandTotals.salePrice;
                    brandsProcessed++;

                    if (brandsProcessed === brands.length) {
                        updateTotalRow();
                    }
                });
            });
        });
    }

    function loadProductsForBrand(brand, brandIndex, callback) {
        $.get(inventoryUrl, { action: 'get_products', brand_id: brand.id }, function(products) {
            let productRows = '';
            const classes = ['table-primary', 'table-secondary', 'table-success', 'table-danger', 'table-warning', 'table-info', 'table-light', 'table-dark'];
            let brandClass = classes[brandIndex % classes.length];

            let brandTotalPurchasePrice = 0;
            let brandTotalSalePrice = 0;

            products.forEach(function(product, index) {
                brandTotalPurchasePrice += parseFloat(product.purchase_price);
                brandTotalSalePrice += parseFloat(product.sale_price);

                productRows += `
                    <tr class="${brandClass}">
                        ${index === 0 ? `<td class="align-middle text-center" rowspan="${products.length}">${brand.brand_name__brand_name}</td>` : ''}
                        ${index === 0 ? `<td class="align-middle text-center" rowspan="${products.length}">
                            ${brand.brand_name__photo ? 
                                `<img src="${brand.brand_name__photo}" alt="${brand.brand_name__brand_name}" style="max-width: 50px; max-height: 50px;">` : 
                                'No image'
                            }
                        </td>` : ''}
                        <td class="align-middle text-center">
                            ${product.photo ? 
                                `<img src="${product.photo}" alt="${product.product_name}" style="max-width: 50px; max-height: 50px;">` : 
                                'No image'
                            }
                        </td>
                        <td class="align-middle text-center">${product.product_name}</td>
                        <td class="align-middle text-center">
                            <span class="badge bg-${product.quantity_in_stock > 10 ? 'success' : 'warning'} rounded-pill">
                                ${product.quantity_in_stock}
                            </span>
                        </td>
                        <td class="align-middle text-center">$${parseFloat(product.purchase_price).toFixed(2)}</td>
                        <td class="align-middle text-center">$${parseFloat(product.sale_price).toFixed(2)}</td>
                    </tr>`;
            });

            $('#productTableBody').append(productRows);
            callback({purchasePrice: brandTotalPurchasePrice, salePrice: brandTotalSalePrice});
        });
    }

    function updateTotalRow() {
        let totalRow = `
            <tr class="table-dark fw-bold">
                <td colspan="5" class="text-end">Total for ${currentCategoryName}:</td>
                <td class="text-center">$${totalPurchasePrice.toFixed(2)}</td>
                <td class="text-center">$${totalSalePrice.toFixed(2)}</td>
            </tr>`;
        $('#categoryTotalRow').html(totalRow);
    }
});