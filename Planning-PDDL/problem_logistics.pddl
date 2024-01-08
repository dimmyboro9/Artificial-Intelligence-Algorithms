(define (problem minecraft-tower)

    (:domain 
        warehouse-logistics    
    )
    
    (:objects
        robot - object
        box - object
        cell - object
        packing_station - object
        
        r1 - robot
        r2 - robot
        
        b1 b2 b3 b4 b5 b6 b7 - box
        
        c00 c01 c02 c03
        c10 c11 c12 c13 
        c20 c21 c22 c23  
        c30 c31 c32 c33 - cell
        
        ps1 ps2 - packing_station
    )

    
    (:init
        (edge c00 c01) (edge c00 c10)
        (edge c01 c00) (edge c01 c02) (edge c01 c11)
        (edge c02 c01) (edge c02 c03) (edge c02 c12)
        (edge c03 c02) (edge c03 c13)
        (edge c10 c00) (edge c10 c11) (edge c10 c20)
        (edge c11 c01) (edge c11 c10) (edge c11 c12) (edge c11 c21)
        (edge c12 c02) (edge c12 c11) (edge c12 c13) (edge c12 c22)
        (edge c13 c03) (edge c13 c12) (edge c13 c23)
        (edge c20 c10) (edge c20 c21) (edge c20 c30)
        (edge c21 c11) (edge c21 c20) (edge c21 c22) (edge c21 c31)
        (edge c22 c12) (edge c22 c21) (edge c22 c23) (edge c22 c32)
        (edge c23 c13) (edge c23 c22) (edge c23 c33)
        (edge c30 c20) (edge c30 c31) 
        (edge c31 c21) (edge c31 c30) (edge c31 c32) 
        (edge c32 c22) (edge c32 c31) (edge c32 c33) 
        (edge c33 c23) (edge c33 c32) 
        
        (station c03 ps1)
        (station c33 ps2)
        
        (on r1 c00)
        (on r2 c33)
        (at b1 c01)
        (at b2 c10)
        (at b3 c02)
        (at b4 c22)
        (at b5 c12)
        (at b6 c30)
        (at b7 c03)
        (occupied_ground c00)
        (occupied_ground c33)
        (occupied_ground c01)
        (occupied_ground c10)
        (occupied_ground c02)
        (occupied_ground c22)
        (occupied_ground c12)
        (occupied_ground c30)
        (occupied_ground c03)
        
        (free_arms r1)
        (free_arms r2)
        
    )
    
    (:goal
        (and 
            (packed b1)
            (packed b2)
            (packed b3)
            (packed b4)
            (packed b5)
            (packed b6)
            (packed b7)
            
        )
    )
)