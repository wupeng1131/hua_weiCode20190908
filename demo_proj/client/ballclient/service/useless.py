def aggressive_alloc(fish_map, power_list, enemy_list, own_list):
    task_list = []

    result_connect = []

    for p in power_list:
        value = p.point
        x = p.x
        y = p.y
        _task = task(x,y,value)
        _task.info = "power_task"
        _task.id = len(task_list)
        task_list.append(_task)
    # find an enemy

    if len(enemy_list) >= 1:
        nearest = 999
        near_enemy = enemy_list[0]
        for e in enemy_list:
            ave_dis = average_distance(own_list, e)
            if ave_dis < nearest:
                nearest = ave_dis
                near_enemy = e                #1.find the nearest enemy

#########accoc catch#####################
        block_map = copy.deepcopy(fish_map)
        for o in own_list:
            block_map.add_own_block(o,near_enemy)
        M_g = graph(fish_map, 0)
        x = near_enemy.x
        y = near_enemy.y
        e_idx = pos2idx(block_map, x, y)
        nodes = M_g.BFS(e_idx, 0, fish_map)
        m = [[99 for i in range(block_map.width)] for j in range(block_map.width)]
        for node in nodes:
            x = node.x
            y = node.y
            step = node.step
            m[y][x] = step                 #2. the range that enemy could reach
        #
        # for _ in m:
        #     print
        #     for a in _:
        #         print("%-3s" % a),
        # print
        print "catch enemy id:",near_enemy.id,"position",near_enemy.x,near_enemy.y


        #####################################
        '''allocate the direction
            input: own list, m, near_emeny,
            output:result_alloc------> the list of connection
            '''

        #1 build dir_task_list
        dir_task_list = []
        dir_value = 1
        add_dir_around_enemy(fish_map, near_enemy, dir_value, dir_task_list)
        #2 build connection_list
        dir_connection_list = []
        # print "len own_list:",len(own_list)
        # print "len dir_task_list:",len(dir_task_list)
        for o in own_list:
            for t in dir_task_list:
                _connection = dir_connection(o, t,fish_map,m)
                # print "connection:", _connection.a, "--->", _connection.direction,"dist:",_connection.dist
                dir_connection_list.append(_connection)

        # print "++++++++++++++++++++++++++++++++++++++++"
        # print_state(own_list)
        # print_task_state(dir_task_list)
        # print "++++++++++++++++++++++++++++++++++++++"
        result_alloc = []
        while to_be_alloc(own_list) and to_be_alloc(dir_task_list):
            # print_state(own_list)
            # print_state(task_list_tmp)
            _connection = choose_connection(dir_connection_list)
            own_id = _connection.a
            task_id = _connection.b
            delete_own(own_id, own_list, dir_connection_list)
            delete_task(task_id, dir_task_list, dir_connection_list)
            result_alloc.append(_connection)
        for o in own_list:
            o.task_state = 0
        # print
        # print "FFFFFFFFFFFFFFFFF",len(result_alloc)
        # print "--------------------------------------"
        # print_state(own_list)
        # print_task_state(dir_task_list)
        # print "--------------------------------------"
        for r in result_alloc:
            print "allocate:",r.a, "--->",direction[r.direction],"dis_a",r.dis_a,"dis_b",r.dis_b,"value",r.value
        print
        print

        ####################################

        # task_list_tmp = []
        # value = 200
        # add_power_around_enemy(fish_map, near_enemy, value, task_list_tmp)
        #
        # connection_list0 = []           # 3. allocate the direction
        # for o in own_list:
        #     for t in task_list_tmp:
        #         _connection = connection(o, t, own_list,fish_map)
        #         # print "connection:", _connection.a, "--->", _connection.direction,"dist:",_connection.dist
        #         connection_list0.append(_connection)
        #
        # result_alloc = []
        # while to_be_alloc(own_list) and to_be_alloc(task_list_tmp):
        #     # print_state(own_list)
        #     # print_state(task_list_tmp)
        #     _connection = choose_connection(connection_list0)
        #     own_id = _connection.a
        #     task_id = _connection.b
        #     delete_own(own_id, own_list, connection_list0)
        #     delete_task(task_id, task_list_tmp, connection_list0)
        #     result_alloc.append(_connection)
        # print
        ##########################################################
        # for r in result_alloc:
        #     print "allocate:",r.a, "--->",r.direction
        #***********alloc directiono -----> catch****************#

        for result in result_alloc:    # 4. set the power for direction
            print "allocate:", result.a, "--->", result.direction
            me = own_list[0]
            for o in own_list:          #4.1 find me by  allocation
                if o.id == result.a:
                    me = o
                    break
            me_dir = result.direction   # 4.2 get direction
            param = 9
            value = 800
            ex = near_enemy.x
            ey = near_enemy.y  #!!!!!!!!!!!!bug!!!!!!!!!!!!!!super bug
            reach_list = could_reach(m,param,me_dir,ex,ey) # 4.3 could reach
            # for node_ in reach_list:
            #     print "&&&node:", "(", node_.x, node_.y, ")"

            if len(reach_list) == 0:  ###what to do with it
                print "no reach_list"
                # _task = task(near_enemy.x, near_enemy.y, value)
                # _task.info = "enemy_target"
                # _task.id = 9999
                # # task_list.append(_task)
                # _connection = connection(me, _task, own_list, fish_map)
                # result_connect.append(_connection)

            # result_connect = []
            # print "***************"

            else:
                state = 0
                count = 0
                for _node in reach_list:                     # 4.4 for each could reach
                    dist1 = me.find_distance(fish_map, _node.x, _node.y)     #djs_distance(fish_map, me.x,me.y,_node.x,_node.y )
                    dist1 = int(dist1)
                    dist2 = _node.step
                    if dist1 == dist2:
                        _task = task(_node.x, _node.y, value)
                        _task.info = "catch_target"
                        _task.id = 8888
                        _connection = connection(me, _task, own_list, fish_map)
                        result_connect.append(_connection)
                        me.task_state = 1
                        state = 1
                        break
                    if dist1 > dist2:
                        if count == 0:
                            _task = task(near_enemy.x, near_enemy.y, value)
                            _task.info = "enemy_stop_target"
                            _task.id = 9999
                            _connection = connection(me, _task, own_list, fish_map)
                            result_connect.append(_connection)
                            state = 1
                            me.task_state = 1
                            break
                        else:
                            _task = task(_node.x, _node.y, value)
                            _task.info = "enemy_stop_target"
                            _task.id = 9999
                            _connection = connection(me, _task, own_list, fish_map)
                            result_connect.append(_connection)
                            state = 1
                            me.task_state = 1
                            break
                    count += 1
                if state == 0:  # bug!!!
                    # print "@@@@@@@@@@@@@@@@@@@@@"
                    count = can_not_go(near_enemy,own_list,fish_map)
                    print count
                    if count == 0:
                        # print "____________________"
                        _task = task(near_enemy.x, near_enemy.y, value)
                        _task.info = "enemy_goto_target"
                        _task.id = 9999
                        _connection = connection(me, _task, own_list, fish_map)
                        me.task_state = 1
                        result_connect.append(_connection)
                    else:
                        _task = task(me.x, me.y, value)
                        _task.info = "enemy_goto_target"
                        _task.id = 9999
                        _connection = connection(me, _task, own_list, fish_map)
                        me.task_state = 1
                        result_connect.append(_connection)






                    # _task = task(_node.x, _node.y, value)
                    # _task.info = "catch_target"
                    # _task.id = 8888
                    # _connection = connection(me, _task, own_list, fish_map)
                    # # print "node:", "(", _node.x, _node.y, ")"
                    # dist1 = me.find_distance(fish_map, _node.x, _node.y)     #djs_distance(fish_map, me.x,me.y,_node.x,_node.y )
                    # dist2 = _node.step
                    #
                    # dist1 = int(dist1)
                    # print "dist1 is:", dist1, "dist2 is :", dist2
                    #
                    # if dist1 == dist2:
                    #
                    #
                    # if dist1 >= dist2:
                    #     if dist1 == dist2 and me.find_distance(fish_map,near_enemy.x, near_enemy.y) ==1:
                    #         _task = task(me.x, me.y, value)
                    #         _task.info = "enemy_stop_target"
                    #         _task.id = 9999
                    #         _connection = connection(me, _task, own_list, fish_map)
                    #         result_connect.append(_connection)
                    #         state = 1
                    #         me.task_state = 1
                    #         break
                    #     else:
                    #         state = 1
                    #         me.task_state = 1
                    #         result_connect.append(_connection)
                    #         break



        # for r in result_connect:
        #     print "alloc$$$$:", r.a, "--->", r.direction, "x", r.dx, "y", r.dy



                    # print "add catch_target",_node.x, _node.y
                    # _task = task(_node.x, _node.y, value)
                    # _task.info = "catch_target"
                    # _task.id = len(task_list)
                    # task_list.append(_task)
                    # break  ####!!!!bug

                    # else:
                    #     _task = task(o.x, o.y, value)
                    #     _task.info = "catch_target"
                    #     _task.id = len(task_list)
                    #     task_list.append(_task)

        # print_task_state(task_list)


    own_list_tmp = []
    for o in own_list:
        if o.task_state == 0:
            own_list_tmp.append(o)

    connection_list = []
    for o in own_list_tmp:
        _task = fish_map.wander_task[o.id]
        _task.id = len(task_list)
        task_list.append(_task)
        _connection = connection(o, _task,own_list,fish_map)
        connection_list.append(_connection)
        for t in task_list:
            if t.info == "wander_task":
                break
            else:
                _connection = connection(o,t,own_list,fish_map)
                connection_list.append(_connection)

    #******************************#
    # print_state(own_list)
    print "&&&&&&&&&&&&&&&",len(own_list_tmp),len(task_list)
    while to_be_alloc(own_list_tmp)  :
        _connection = choose_connection(connection_list)
        # print "choose",_connection.a,"---->", _connection.b, _connection.value
        own_id = _connection.a
        task_id = _connection.b
        delete_own(own_id, own_list, connection_list)
        delete_task(task_id, task_list, connection_list)
        result_connect.append(_connection)
    # for r in result_connect:
    #     print "result!!!:", r.a, "--->", r.direction, "x", r.dx, "y", r.dy

    #########################################







        #
        #
        # # for _ in m:
        # #     print
        # #     for a in _:
        # #         print("%-3s" % a),
        # set_n = 4
        # dir_list = []
        # for o in own_list:
        #     enemy2own = judge_task(near_enemy,o)#{1:up 2:down 3:left 4:right}
        #     # if not dir_overlap(dir_list,dir_enemy2own):
        #     # dir_list.append(dir_enemy2own)
        #     dis = distance_(o.x,o.y,near_enemy.x,near_enemy.y)
        #     print "enemy id:", near_enemy.id,"own id:",o.id,"catch_direction:",enemy2own
        #     dis_count = int(dis/2)
        #     x,y = search_limit(m,near_enemy.x,near_enemy.y,enemy2own, dis_count)
        #     value = 100
        #     _task = task(x, y, value)
        #     _task.info = "enemy_power"
        #     _task.id = len(task_list)
        #     task_list.append(_task)







        #
        # value = 0.9
        # x = near_enemy.x
        # y = near_enemy.y
        # _task = task(x, y, value)
        # _task.info = "enemy_task"
        # _task.id = len(task_list)
        # task_list.append(_task)
        # add_power_around_enemy(fish_map, near_enemy, value, task_list)




        # for e in enemy_list:
        #     # ave_dis = average_distance(fish_map,own_list,e)
        #     value = 100
        #     print "value of enemy:",e.id, "is",value
        #     x = e.x
        #     y = e.y
        #     _task = task(x, y, value)
        #     _task.info = "enemy_task"
        #     _task.id = len(task_list)
        #     task_list.append(_task)
        #     add_power_around_enemy(fish_map,e,value,task_list)

    # own_list----------task_list
    # connection_list = []
    # for o in own_list:
    #     for t in task_list:
    #         _connection = connection(o, t, own_list, fish_map)
    #         connection_list.append(_connection)

        #
        # _task = fish_map.wander_task[o.id]
        # _task.id = len(task_list)
        # task_list.append(_task)
        # _connection = connection(o, _task,own_list,fish_map)
        # connection_list.append(_connection)
        # for t in task_list:
        #     if t.info == "wander_task":
        #         break
        #     else:
        #         _connection = connection(o,t,own_list,fish_map)
        #         connection_list.append(_connection)



    #connection
    # result_alloc = []
    # print "the length of task list is ",len(task_list)
    # for t in task_list:
    #     print "(","id",t.id,t.x,t.y,")",
    # print "$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$"
    # print "the length of own list is ",len(own_list)
    # print "the lenght of connection is:", len(connection_list)
    # for t in own_list:
    #     print "(","id",t.id,t.x,t.y,")",
    ###bug!!!!!! own_list should restore
    # for o in own_list:
    #     o.task_state = 0
    # while to_be_alloc(own_list) and to_be_alloc(task_list) :
    #     # print_state(own_list)
    #     # print "^^^^^^^^^^^^^"
    #     # print_task_state(task_list)
    #     # print "WWWWWWWWWWWWWWWWWWWWWWWWWWWWW"
    #     _connection = choose_connection(connection_list)
    #     # print "choose",_connection.a,"---->", _connection.b, _connection.value
    #     own_id = _connection.a
    #     task_id = _connection.b
    #     delete_own(own_id, own_list, connection_list)
    #     delete_task(task_id, task_list, connection_list)
    #     result_alloc.append(_connection)
    # for result in result_alloc:
    #     print "XXXXXXXXXXXXX",result.a,result.b
    return result_connect