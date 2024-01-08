(define (domain warehouse-logistics)
    
    (:types
        object packing_station robot box cell
    )
    
    (:predicates
        (edge ?cell ?cell)
        (station ?cell ?packing_station)
        
        (occupied_ground ?cell)
        (occupied_air ?cell)
        (on ?robot ?cell)
        (over ?robot ?cell)
        (at ?box ?cell)
                               
        (keep ?robot ?box)
        (free_arms ?robot)
        (packed ?box)
    )
    
    (:action move
        :parameters 
            (?robot
             ?from 
             ?to)

        :precondition 
            (and 
                (on ?robot ?from)
                (edge ?from ?to)
                (not (occupied_ground ?to))
            )

        :effect 
            (and 
                (on ?robot ?to)
                (not (on ?robot ?from))
                (occupied_ground ?to)
                (not (occupied_ground ?from))
            )
    )
    
    (:action fly
        :parameters 
            (?robot
             ?from
             ?to)

        :precondition 
            (and 
                (over ?robot ?from)
                (edge ?from ?to)
                (not (occupied_air ?to))
            )

        :effect 
            (and 
                (over ?robot ?to)
                (not (over ?robot ?from))
                (occupied_air ?to)
                (not (occupied_air ?from))
            )
    )
    
    (:action takeoff
        :parameters 
            (?robot
             ?position)

        :precondition 
            (and 
                (on ?robot ?position)
                (not (occupied_air ?position))
            )

        :effect 
            (and 
                (over ?robot ?position)
                (not (on ?robot ?position))
                (occupied_air ?position)
                (not (occupied_ground ?position))
            )
    )
    
    (:action land
        :parameters 
            (?robot
             ?position)

        :precondition 
            (and 
                (over ?robot ?position)
                (not (occupied_ground ?position))
            )

        :effect 
            (and 
                (on ?robot ?position)
                (not (over ?robot ?position))
                (occupied_ground ?position)
                (not (occupied_air ?position))
            )
    )
    
    (:action take
        :parameters
            (?robot
             ?box
             ?robot_position
             ?box_position)
        
        :precondition 
            (and 
                (edge ?robot_position ?box_position)
                (on ?robot ?robot_position)
                (at ?box ?box_position)
                (free_arms ?robot)
            )
            
        :effect 
            (and 
                (not (at ?box ?box_position))
                (not (free_arms ?robot))
                (not (occupied_ground ?box_position))
                (keep ?robot ?box)
            )
    )
    
    (:action put_on_ground
        :parameters
            (?robot
             ?box
             ?robot_position
             ?box_position)
        
        :precondition 
            (and 
                (edge ?robot_position ?box_position)
                (on ?robot ?robot_position)
                (not (occupied_ground ?box_position))
                (keep ?robot ?box)
                (not (free_arms ?robot)) ;; maybe without it
            )
            
        :effect 
            (and 
                (at ?box ?box_position)
                (occupied_ground ?box_position)
                (free_arms ?robot)
                (not (keep ?robot ?box))
            )
    )
    
    (:action pack
        :parameters
            (?robot
             ?box
             ?robot_position
             ?station)
        
        :precondition 
            (and 
                (station ?robot_position ?station)
                (on ?robot ?robot_position)
                (keep ?robot ?box)
                (not (free_arms ?robot)) ;;maybe without it
            )
            
        :effect 
            (and 
                (packed ?box)
                (free_arms ?robot)
                (not (keep ?robot ?box))
            )
    )
)