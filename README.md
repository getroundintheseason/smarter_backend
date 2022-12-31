# API
### Order LIST
-  Http method GET<br>
    /api/v1/orders

### GET Single Order    
-  Http method GET<br>
    /api/v1/order/{order_id}
    
### UPDATE Single Order  
-  Http method POST<br>
    /api/v1/order/{order_id}

# RUN
    uvicorn app:app --reload --host 0.0.0.0
