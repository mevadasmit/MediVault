### BASE ###
USER = "user"
USER_PROVIDE = "User must be provided when creating a new ProductCategory."
CREATED_BY = "created_by"
UPDATED_BY = "updated_by"
QUANTITY_IN_STOCK = "quantity_in_stock"
ORDER_BY_CREATED = "-created_at"
IS_ACTIVE = "is_active"
IS_SUPERUSER = "is_superuser"
IS_STAFF = "is_staff"

### FORMS ###

FIELD_NAME = "name"
FIELD_ADDRESS = "address"
FILED_FIRST_NAME = "first_name"
FIELD_LAST_NAME = "last_name"
FIELD_EMAIL = "email"
FIELD_PHONE_NUMBER = "phone_number"
FIELD_SUPPLIER = "supplier"
FIELD_ROLE = "role"
FIELD_IS_EMERGENCY = "is_emergency"
FIELD_INVENTORY = "inventory"
FIELD_QUANTITY_REQUESTED = 'quantity_requested'
FIELD_QUANTITY = 'quantity'
FILED_STATUS = "status"
FILED_TOTAL_PRICE = "total_price"
ID = "id"

OLD_PASSWORD = "old_password"
NEW_PASSWORD = "new_password"
CONFIRM_PASSWORD = "confirm_password"

### ROLES ###
NURSE = "Nurse"
SUPPLIER = "Supplier"
INVENTORY__MANAGER = "Inventory Manager"
ADMIN = "Admin"

### HTTPS ###
REQUEST = "request"
POST = "post"
HTTP_REFERER = "HTTP_REFERER"
ACTION = "action"

### MESSAGES ###

ADDED_TO_CART_SUCCESS = "Added {item_name} to cart."
ITEM_REMOVED = "Item removed from cart."
CART_IS_EMPTY = "Your cart is empty. Add items before placing an order."
PASSWORD_NOT_MATCH = "Passwords don't match"
EMAIL_MUST_BE_SENDED = "The email must be set"

###  MAIN ADMIN  ###
VALIDATION_ERROR = "Not enough inventory available."


### INVENTORY MANAGER ###

INVENTORY_MANAGER = "inventory_manager"
VALIDATION_ERROR_IM = "Only an Inventory Manager can register a Nurse."

SELECT_SUPPLIER = "Select Supplier"
SELECT_ROLE = "Select Role"
SELECT_PRODUCT = "Select Product"
EMERGENCY_REQUEST = "Emergency Request"
QUANTITY = "Quantity"
INVENTORY = "Inventory"
STATUS = "Status"
INCREASE = "increase"
DECREASE = "decrease"
SUBMIT = "Submit"
REGISTER = "Register"

SELECT_AVAILABLE_SUPPLIER = "Select Available Supplier"

#--- URLS ---#

NURSE_MANAGEMENT = "nurse_management"
INVENTORY_MANAGEMENT = "inventory_manager"
RETURNABLE_ITEMS = "returnable_items"

#--- TEMPLATES ---#

INVENTORY_MANAGER_DASHBOARD = "inventory_manager/dashboard.html"
INVENTORY_NURSE_MANAGEMENT = "inventory_manager/nurse_management.html"
INVENTORY_NURSE_REGISTER = "inventory_manager/nurse_register.html"
INVENTORY_NURSE_UPDATE = "inventory_manager/nurse_update.html"
INVENTORY_NURSE_DELETE = "inventory_manager/nurse_confirm_delete.html"
INVENTORY_MANAGEMENTS = "inventory_manager/inventory_management.html"
INVENTORY_SUPPLIER_SELECTION = "inventory_manager/supplier_selection.html"
INVENTORY_SUPPLIER_INVENTORY = "inventory_manager/supplier_inventory.html"
INVENTORY_REQUEST_LIST = "inventory_manager/request_list.html"
INVENTORY_RETURN_LIST = "inventory_manager/returnable_items.html"
INVENTORY_REQUEST_DETAILS = "inventory_manager/request_details.html"


ADMIN_DASHBOARD = "admin/dashboard.html"
ADMIN_NEW_USER_REGISTER = "admin/register_success.html"
ADMIN_USER_MANAGEMENT = "admin/user_management.html"
ADMIN_USER_UPDATE = "admin/update_user.html"
ADMIN_USER_DELETE = "admin/user_confirm_delete.html"
ADMIN_ORGANIZATION_MANAGEMENT = "admin/organizations_management.html"
ADMIN_ORGANIZATION_REGISTER = "admin/organization_registration.html"
ADMIN_ORGANIZATION_UPDATE = "admin/update_organization.html"
ADMIN_ORGANIZATION_DELETE = "admin/organization_confirm_delete.html"
ADMIN_INVENTORY_CATEGORY = "admin/product_category_list.html"
ADMIN_INVENTORY_CATEGORY_FORM = "admin/product_category_form.html"
ADMIN_INVENTORY_CATEGORY_UPDATE = "admin/product_category_update.html"
ADMIN_INVENTORY_CATEGORY_DELETE = "admin/product_category_confirm_delete.html"


NURSE_DASHBOARD = "nurse/dashboard.html"
NURSE_REQUEST_CART = "nurse/request_cart.html"
NURSE_REQUEST_LIST = "nurse/request_list.html"
NURSE_REQUEST_DETAILS = "nurse/request_details.html"


ORDER_CART = "orders/cart.html"
ORDER_CONFIRMATION = "orders/order_confirmation.html"
ORDER_DETAILS =  "orders/order_details.html"
ORDER_LIST = "orders/order_list.html"
ORDER_UPDATE = "orders/order_update.html"

SUPPLIER_DASHBOARD = "supplier/dashboard.html"
SUPPLIER_MANAGEMENT = "supplier/supplier_management.html"
SUPPLIER_ORDER_DETAILS = "supplier/supplier_order_details.html"
SUPPLIER_ORDER_UPDATE = "supplier/supplier_order_update.html"

BASE_DASHBOARD = "base/base.html"
BASE_REGISTER = "base/register.html"

USER_REGISTER = "users/register.html"
USER_LOGIN = 'users/login.html'
USER_CHANGE_PASSWORD = "users/change_password.html"
USER_PROFILE_UPDATE = "users/profile_update.html"

#--- OBJECTS_NAME ---#

CART_ITEMS_BY_SUPPLIER = "cart_items_by_supplier"
CART = "cart"
NURSES = "nurses"
USERS = "users"
INVENTORY_ITEMS = "inventory_items"
ORGANIZATIONS = "organizations"
INVENTORY_CATEGORY = "product_categories"
CART_ITEMS = "cart_items"
REQUESTS = "requests"
ROLE = "role"
ROLE_COUNTS = "role_counts"
ROLE_NAME = "role__name"
ITEM_FORM = "item_form"
AVAILABLE_INVENTORY = "available_inventory"
GET_INVENTORY = "inventory[]"
QUANTITY_REQUESTED = "quantity_requested[]"
ORDER = "order"
ORDERS = "orders"
ORDER_ITEMS = "order_items"
SUPPLIER_ORDERS = "supplier_orders"

### ID'S  ###

SUPPLIER_ID = "supplier_id"
INVENTORY_ID = "inventory_id"
REQUEST_ID = "request_id"
REQUESTED_ITEM_ID = "requested_item_id"
ORDER_ID = "order_id"

### STATUS  ###

PENDING = "Pending"
DELIVERED = "Delivered"
CONFIRMED = "Confirmed"
APPROVED = "Approved"
REJECTED = "Rejected"
CANCELLED = "Cancelled"
