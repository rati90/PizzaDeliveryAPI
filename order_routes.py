from fastapi import APIRouter, Depends, status
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from tools import authorization_token

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = Session(bind=engine)


@order_router.get('/')
async def hello(Authorize: AuthJWT = Depends()):
    error_message = 'Invalid Token'
    await authorization_token(Authorize, error_message)

    return {'message': 'hello World'}


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    error_message = 'Invalid Token'
    await authorization_token(Authorize, error_message)

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity
    )

    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        'order_status': new_order.order_status
    }

    return jsonable_encoder(response)


@order_router.get('/orders')
async def list_all_order(Authorize: AuthJWT = Depends()):
    error_message = 'Invalid Token'
    await authorization_token(Authorize, error_message)

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()

        return jsonable_encoder(orders)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="You are not a superuser"
                        )


@order_router.get('/orders/{id}')
async def get_order_by_id(id: int, Authorize: AuthJWT = Depends()):
    error_message = 'Please provide a valid token'
    await authorization_token(Authorize, error_message)

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    if current_user.is_staff:
        order = session.query(Order).filter(Order.id == id).first()

        return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="User not allowed to carry out request"
                        )


@order_router.get('/user/orders')
async def get_user_order(Authorize: AuthJWT = Depends()):
    error_message = 'Invalid Token'
    await authorization_token(Authorize, error_message)

    user = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == user).first()

    return jsonable_encoder(current_user.orders)


@order_router.get('/user/order/{id}/')
async def get_specific_order(id: int, Authorize: AuthJWT = Depends()):
    error_message = 'Invalid Token'
    await authorization_token(Authorize, error_message)

    subject = Authorize.get_jwt_subject()

    current_user = session.query(User).filter(User.username == subject).first()

    orders = current_user.orders
    print('rrrR')

    for order in orders:
        if order.id == id:
            return jsonable_encoder(order)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail="No order with this id"
                        )


@order_router.put('/order/update/{id}')
async def update_order(id: int, order: OrderModel, Authorize: AuthJWT = Depends()):
    error_message = 'Invalid Token'
    await authorization_token(Authorize, error_message)

    order_to_update = session.query(Order).filter(Order.id == id).first()

    order_to_update.quantity = order.quantity
    order_to_update.pizza_size = order.pizza_size

    session.commit()

    response = {
        "id": order_to_update.id,
        "quantity": order_to_update.quantity,
        "pizza_size": order_to_update.pizza_size,
        "order_status": order_to_update.order_status,
    }

    return jsonable_encoder(response)


@order_router.patch('/order/status/{id}')
async def update_order_status(id: int, order: OrderStatusModel,
                              Authorize: AuthJWT = Depends()
                              ):
    error_message = 'Invalid Token'
    await authorization_token(Authorize, error_message)

    username = Authorize.get_jwt_subject()
    current_user = session.query(User).filter(User.username == username).first()

    if current_user.is_staff:
        order_to_update = session.query(Order).filter(Order.id == id).first()

        order_to_update.order_status = order.order_status

        session.commit()

        response = {
            "id": order_to_update.id,
            "quantity": order_to_update.quantity,
            "pizza_size": order_to_update.pizza_size,
            "order_status": order_to_update.order_status,
        }

        return jsonable_encoder(response)


