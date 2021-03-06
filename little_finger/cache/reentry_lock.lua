---
--- Generated by EmmyLua(https://github.com/EmmyLua)
--- Created by weihao.lv.
--- DateTime: 2021/5/26 2:56 下午
--- 可重入加锁

-- 加锁
-- 加锁键
local lockKey = KEYS[1]
-- 代表重入请求的唯一 id
local requestId = ARGV[1]

if redis.call('EXISTS', lockKey) ~= 0 then
    local lockTable = redis.call("HMGET", lockKey, 'requestId', 'count')
    if (requestId ~= lockTable[1]) then
        return 0
    else
        redis.call('HMSET', lockKey, 'count', lockTable[2] + 1)
        return 1
    end
else
    redis.call("HMSET", lockKey, 'requestId', requestId, 'count', 1)
    redis.call("EXPIRE", lockKey, 30)
    return 1
end





--[[
    通过 lua 脚本加锁能够解决可重入问题，但是依然无法解决以下问题
    1. 锁超时后自动释放被其他请求再次获取，导致两个进行中的请求同时认为自己持有锁，导致并发问题。
        这个问题仅依靠 redis server端无法解决，server 端无法感知当前的请求是否会超时，无法主动延长加锁时间。
        所以还是需要在客户端主动感知请求没有主动解锁，延后延迟加锁。

    2. 由于 redis 主节点挂掉，导致主从切换，同时由于同步问题，锁数据未被同步，导致两个请求同时认为自己持有锁，导致并发问题。
        这个场景是由于 redis 本身的集群架构模式导致的，需要通过 redlock 等算法，获取基于集群的锁才能解决这个问题。
]]--
